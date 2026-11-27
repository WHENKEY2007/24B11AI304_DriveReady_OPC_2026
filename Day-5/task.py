"""
Day 5: Retrieval-Augmented Generation (RAG), ChromaDB & Thread-Isolated Agents
Balu Tailors Workshop Assistant: Vector Embeddings, Business Knowledge Retrieval,
LangChain Tools, and LangGraph State Checkpointing.
"""

import os
import json
import getpass
from typing import Optional, Literal, Dict, Any, List
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Setup Groq API Key
if "GROQ_API_KEY" not in os.environ:
    try:
        from google.colab import userdata
        os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")
    except Exception:
        api_key = getpass.getpass("Enter your Groq API key: ")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key

try:
    from langchain_groq import ChatGroq
    from langchain.tools import tool
    from langchain.agents import create_agent
    from langchain_core.documents import Document
    from langgraph.checkpoint.memory import InMemorySaver
except ImportError:
    raise ImportError(
        "Please install dependencies: pip install langchain langchain-groq pydantic "
        "langchain-chroma langchain-huggingface sentence-transformers langgraph"
    )

# Initialize ChatGroq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.2,
    max_retries=3
)

# ---------------------------------------------------------------------------
# Google Sheets Setup (with In-Memory Fallback for Local / Non-Colab Execution)
# ---------------------------------------------------------------------------
worksheets: Dict[str, Any] = {}

class LocalWorksheetFallback:
    """Mock worksheet providing get_all_records and append_row for local execution."""
    def __init__(self, title: str, headers: List[str]):
        self.title = title
        self.headers = headers
        self.data: List[List[Any]] = [headers]

    def get_all_records(self) -> List[Dict[str, Any]]:
        if len(self.data) < 2:
            return []
        keys = self.data[0]
        return [dict(zip(keys, row)) for row in self.data[1:]]

    def get_all_values(self) -> List[List[Any]]:
        return self.data

    def append_row(self, row: List[Any]):
        self.data.append(row)


def init_storage():
    """Initialize Google Sheets via gspread or fallback to in-memory store."""
    global worksheets
    try:
        from google.colab import auth
        from google.auth import default
        import gspread

        auth.authenticate_user()
        creds, _ = default()
        gc = gspread.authorize(creds)
        sheet_name = "Balu Tailors Day5 Practice"
        try:
            sh = gc.open(sheet_name)
        except gspread.SpreadsheetNotFound:
            sh = gc.create(sheet_name)

        headers_map = {
            "customers": ["id", "customer_code", "name", "phone", "notes", "created_at", "updated_at"],
            "orders": [
                "id", "order_number", "customer_id", "garment_type", "order_date",
                "delivery_date", "status", "price", "advance", "notes", "measurements",
                "worker_id", "worker_name", "cutting_status", "stitching_status",
                "worker_rate", "cloth_photo", "cloth_color", "group_id", "pair_label",
                "created_at", "updated_at"
            ],
            "price_settings": [
                "id", "shirt_price", "pant_price", "pair_price",
                "kurta_price", "blouse_price", "safari_price", "updated_at"
            ]
        }
        existing = [w.title for w in sh.worksheets()]
        for t, h in headers_map.items():
            if t in existing:
                ws = sh.worksheet(t)
                if not ws.get_all_values():
                    ws.append_row(h)
            else:
                ws = sh.add_worksheet(title=t, rows=1000, cols=len(h))
                ws.append_row(h)
            worksheets[t] = ws

        if len(worksheets["price_settings"].get_all_values()) < 2:
            worksheets["price_settings"].append_row(["default", 400, 450, 800, 550, 400, 750, ""])

        print(f"Connected to Google Sheets: {sh.url}")
    except Exception:
        # Local fallback
        headers_map = {
            "customers": ["id", "customer_code", "name", "phone", "notes", "created_at", "updated_at"],
            "orders": [
                "id", "order_number", "customer_id", "garment_type", "order_date",
                "delivery_date", "status", "price", "advance", "notes", "measurements",
                "worker_id", "worker_name", "cutting_status", "stitching_status",
                "worker_rate", "cloth_photo", "cloth_color", "group_id", "pair_label",
                "created_at", "updated_at"
            ],
            "price_settings": [
                "id", "shirt_price", "pant_price", "pair_price",
                "kurta_price", "blouse_price", "safari_price", "updated_at"
            ]
        }
        for t, h in headers_map.items():
            worksheets[t] = LocalWorksheetFallback(t, h)
        worksheets["price_settings"].append_row(["default", 400, 450, 800, 550, 400, 750, ""])
        worksheets["customers"].append_row(["C001", "CUST-001", "Ravi Kumar", "9876543210", "Regular", "2026-11-26", ""])
        worksheets["customers"].append_row(["C002", "CUST-002", "Suresh", "9123456780", "New", "2026-11-26", ""])


init_storage()

# ---------------------------------------------------------------------------
# Business Tools & Pydantic Schema
# ---------------------------------------------------------------------------
class TailoringOrder(BaseModel):
    id: str = Field(min_length=1, description="Unique order ID")
    customer_id: str = Field(min_length=1, description="Existing customer ID")
    garment_type: str = Field(min_length=1, description="Garment type")
    order_date: str = Field(min_length=1, description="YYYY-MM-DD")
    delivery_date: str = Field(min_length=1, description="YYYY-MM-DD")
    measurements: str = Field(min_length=1)
    price: float = Field(ge=0)
    advance: float = Field(default=0, ge=0)
    notes: str = ""
    cloth_color: str = ""
    worker_id: str = ""
    worker_name: str = ""
    group_id: str = ""
    pair_label: str = ""


def read_prices() -> Dict[str, float]:
    rows = worksheets["price_settings"].get_all_records()
    if not rows:
        return {}
    row = rows[-1]
    return {
        "shirt": float(row.get("shirt_price") or 0),
        "pant": float(row.get("pant_price") or 0),
        "pair": float(row.get("pair_price") or 0),
        "kurta": float(row.get("kurta_price") or 0),
        "safari": float(row.get("safari_price") or 0),
    }


@tool
def get_price(garment_type: str, quantity: int = 1) -> str:
    """Get the base price for a shirt, pant, pair, kurta or safari suit.

    Use this tool when the shop owner or customer asks for a configured base price.
    Blouse stitching is not offered by Balu Tailors.

    Args:
        garment_type: shirt, pant, pair, kurta or safari.
        quantity: Number of garments.
    """
    if quantity < 1:
        return "Quantity must be at least 1."
    key = garment_type.lower().strip()
    aliases = {
        "shirts": "shirt", "trousers": "pant", "pants": "pant",
        "kurti": "kurta", "kurtis": "kurta", "safari suit": "safari"
    }
    key = aliases.get(key, key)
    prices = read_prices()
    if key not in prices:
        return "No configured price for that garment. Please confirm with Balu Tailors."
    if prices[key] <= 0:
        return f"No price is configured for {key} yet."
    return f"{quantity} {key}(s): Rs. {prices[key] * quantity:.2f} (base price)"


@tool
def find_customer(search_text: str) -> str:
    """Find a Balu Tailors customer by name, phone number or customer ID.

    Use before logging an order to identify an existing customer.

    Args:
        search_text: Customer name, phone number or customer ID.
    """
    q = search_text.lower().strip()
    if not q:
        return "Please provide a customer name, phone number or ID."
    rows = worksheets["customers"].get_all_records()
    matches = [
        row for row in rows
        if q in str(row.get("id", "")).lower()
        or q in str(row.get("name", "")).lower()
        or q in str(row.get("phone", "")).lower()
    ]
    return str(matches[:10]) if matches else "No matching customer found."


@tool
def log_order(
    id: str,
    customer_id: str,
    garment_type: str,
    order_date: str,
    delivery_date: str,
    measurements: str,
    price: float,
    advance: float = 0,
    notes: str = "",
    worker_id: str = "",
    worker_name: str = "",
    cloth_color: str = "",
    group_id: str = "",
    pair_label: str = ""
) -> str:
    """Validate and save one confirmed tailoring order to the Google Sheets orders tab.

    Use only after the customer ID, garment, dates, measurements and agreed price
    have been confirmed. One garment is saved per row.

    Args:
        id: Unique order ID.
        customer_id: Existing customer ID.
        garment_type: Garment being stitched.
        order_date: Order date in YYYY-MM-DD format.
        delivery_date: Delivery date in YYYY-MM-DD format.
        measurements: Confirmed garment measurements.
        price: Agreed price.
        advance: Advance received, if any.
        notes: Additional notes.
        worker_id: Assigned worker ID, if any.
        worker_name: Assigned worker name, if any.
        cloth_color: Cloth colour.
        group_id: Shared ID for related garments, if any.
        pair_label: Label for this garment within a group, if any.
    """
    try:
        record = TailoringOrder(
            id=id, customer_id=customer_id, garment_type=garment_type,
            order_date=order_date, delivery_date=delivery_date,
            measurements=measurements, price=price, advance=advance,
            notes=notes, worker_id=worker_id, worker_name=worker_name,
            cloth_color=cloth_color, group_id=group_id, pair_label=pair_label
        )
        worksheets["orders"].append_row([
            record.id, "", record.customer_id, record.garment_type,
            record.order_date, record.delivery_date, "Pending", record.price,
            record.advance, record.notes, record.measurements, record.worker_id,
            record.worker_name, "Pending", "Pending", "", "",
            record.cloth_color, record.group_id, record.pair_label, "", ""
        ])
        return f"Order {record.id} saved successfully for customer {record.customer_id}."
    except Exception as e:
        return f"Order was not saved: {e}"


# ---------------------------------------------------------------------------
# Business Knowledge Base (RAG Chunks & Embeddings)
# ---------------------------------------------------------------------------
tailoring_facts = [
    "Balu Tailors provides custom tailoring services.",
    "Balu Tailors offers kurti stitching services.",
    "Balu Tailors offers chudidar stitching services.",
    "Balu Tailors provides pant stitching services.",
    "Balu Tailors provides pant alteration services.",
    "Balu Tailors offers dress stitching services.",
    "Customers can request customized designs for their garments.",
    "Customers can discuss their preferred neck designs before stitching.",
    "Customers can discuss their preferred sleeve designs before stitching.",
    "Customers should provide accurate body measurements for proper fitting.",
    "Customers can discuss their preferred garment style before stitching begins.",
    "Customers can provide their own fabric for stitching.",
    "Customers can share reference images of their preferred designs.",
    "Customers can ask the shop about the progress of their stitching orders.",
    "Customers should contact Balu Tailors to confirm prices, service availability and delivery dates."
]

documents = [
    Document(
        page_content=fact,
        metadata={"fact_number": i + 1, "business": "Balu Tailors"}
    )
    for i, fact in enumerate(tailoring_facts)
]

# Initialize Vector Store
vector_store = None
try:
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    chroma_dir = os.path.join(os.path.expanduser("~"), ".chroma_balu_tailors")
    collection_name = "balu_tailors_knowledge"

    try:
        old_store = Chroma(
            collection_name=collection_name,
            persist_directory=chroma_dir,
            embedding_function=embedding_model
        )
        old_store.delete_collection()
    except Exception:
        pass

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        collection_name=collection_name,
        persist_directory=chroma_dir
    )
except Exception as e:
    print(f"Chroma/Embedding notice: {e}. Using simple keyword fallback.")


def retrieve_context(question: str, top_k: int = 4) -> str:
    """Retrieve relevant business facts from Chroma vector store or keyword fallback."""
    if vector_store is not None:
        try:
            results = vector_store.similarity_search(question, k=top_k)
            if results:
                return "\n".join(f"- {doc.page_content}" for doc in results)
        except Exception:
            pass

    # Simple keyword fallback if vector store is unavailable
    q_words = set(question.lower().split())
    matches = [
        f for f in tailoring_facts
        if any(w in f.lower() for w in q_words if len(w) > 3)
    ]
    if matches:
        return "\n".join(f"- {m}" for m in matches[:top_k])
    return "No relevant business information was found."


@tool
def search_business_knowledge(question: str) -> str:
    """Search Balu Tailors' business knowledge for services, designs, measurements,
    customer-provided fabric, reference images, order progress, and price or
    delivery enquiries. Use for general business questions. This knowledge base
    does not contain confirmed prices or guaranteed delivery dates.

    Args:
        question: The customer's or shop owner's business question.
    """
    return retrieve_context(question)


# ---------------------------------------------------------------------------
# LangGraph Agent with RAG & Thread Checkpointing
# ---------------------------------------------------------------------------
SYSTEM = """You are the Balu Tailors workshop assistant.

TOOLS:
- Use get_price for configured base garment prices.
- Use find_customer to look up customers.
- Use log_order only after all required order details are known and confirmed.
- Use search_business_knowledge for general tailoring business questions.

RAG RULES:
- Use retrieved business facts as evidence when answering general business questions.
- If the retrieved facts do not answer the question, say:
  'I don't have that information. Please confirm with Balu Tailors.'
- Never invent services, prices, measurements, shop timings or delivery promises.
- Balu Tailors does NOT offer blouse stitching or blouse alteration.
- Use get_price for actual configured prices; do not rely on a general fact for a price.

ORDER RULES:
- Never invent customer IDs, measurements, dates or prices.
- Ask follow-up questions when required details are missing.
- Use log_order only after customer ID, garment, dates, measurements and agreed price
  have been confirmed.
- This notebook uses Google Sheets for practice; it is not connected to live Supabase.

Be clear, concise and friendly.
"""

checkpointer = InMemorySaver()

agent = create_agent(
    model=llm,
    tools=[get_price, find_customer, log_order, search_business_knowledge],
    system_prompt=SYSTEM,
    checkpointer=checkpointer
)


def chat_with_thread(message: str, thread_id: str = "customer_1") -> str:
    """Send user query to the agent maintaining thread-level isolation."""
    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config={"configurable": {"thread_id": thread_id}}
        )
        last_message = result["messages"][-1]
        content = getattr(last_message, "content", "")
        return content if isinstance(content, str) else str(content)
    except Exception as e:
        return f"Error: {e}"


# ---------------------------------------------------------------------------
# Execution & Test Suite
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("DAY 5: Testing RAG Knowledge Retrieval & Agent Guardrails")
    print("=" * 60)

    test_questions = [
        "What tailoring services do you offer?",
        "Do you provide pant alterations?",
        "Do you stitch blouses?",
        "What is the exact price of a kurti?",
        "Can you guarantee delivery tomorrow?"
    ]

    for question in test_questions:
        print("\nQUESTION:", question)
        print("ANSWER:", chat_with_thread(question, "test_customer"))

    print("\n" + "=" * 60)
    print("DAY 5: Thread Separation & Memory Isolation Test")
    print("=" * 60)
    print("Customer A (introducing):", chat_with_thread(
        "My name is Test Customer A.", "customer_A"
    ))
    print("Customer B (querying unshared name):", chat_with_thread(
        "What name did I tell you?", "customer_B"
    ))
    print("Customer A (querying own name):", chat_with_thread(
        "What name did I tell you?", "customer_A"
    ))
