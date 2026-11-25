"""
Day 3: Advanced Agent Workflows & Conversational Memory
Tailoring Assistant with LCEL Memory Chain, Benchmark Evaluation, and LangChain Agent Architecture.
"""

import os
import csv
import getpass
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure Google API Key
if "GOOGLE_API_KEY" not in os.environ:
    try:
        from google.colab import userdata
        os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
    except Exception:
        api_key = getpass.getpass("Enter your Google API key: ")
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.output_parsers import StrOutputParser
except ImportError:
    raise ImportError("Please install dependencies: pip install langchain-google-genai langchain-core langchain")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
    temperature=0.2
)

# System Prompt with Domain-Specific Facts, Behavioral Rules, and Formatting
SYSTEM = """
ROLE:
You are a friendly assistant for a men's tailoring business.

FACTS:
- Services include:
  1. Shirt stitching
  2. Pant stitching
  3. Trouser stitching
  4. Suit stitching
  5. Blazer stitching
  6. Kurta stitching
  7. Clothing alterations
  8. Custom men's outfits
- Custom measurements are required for stitching.
- Pricing depends on garment type, fabric, and design.
- Customers can enquire about stitching services and prices.

RULES:
- Only discuss men's tailoring services.
- Never invent prices or delivery dates.
- Never promise delivery times or locations.
- If information is unavailable, say:
  "I'll check with the tailor."
- Ask for garment type and design details
  before discussing pricing.
- Be polite and professional.
- Do not assume fabric is provided by the shop.

FORMAT:
- Keep responses under 50 words.
- Use simple English or Telugu,
  matching the customer's language.
- Use a friendly, conversational tone.
"""

# Multi-turn Prompt Template with Memory Placeholder
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM),
    MessagesPlaceholder("history"),  # Conversational history goes here
    ("human", "{question}"),
])

# LangChain Expression Language (LCEL) Chain
chain = prompt | llm | StrOutputParser()

# Conversational state memory
history = []


def ask(question: str) -> str:
    """Send a user query to the tailoring assistant and update conversational memory."""
    answer = chain.invoke({"history": history, "question": question})
    history.extend([("human", question), ("ai", answer)])
    return answer


def run_tests(path: str = "test.csv") -> None:
    """Run automated evaluation against a benchmark dataset."""
    if not os.path.exists(path):
        print(f"Test file '{path}' not found. Skipping CSV benchmark.")
        return

    with open(path, mode="r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    passed = 0
    for row in rows:
        answer = chain.invoke({"history": [], "question": row["question"]})
        ok = row.get("must_include", "").lower() in answer.lower()
        passed += ok
        print("PASS" if ok else "FAIL", "|", row["question"], "→", answer[:70])
    print(f"\n{passed}/{len(rows)} passed ({passed / len(rows):.0%})")


def create_tailoring_agent():
    """Create tailoring assistant using LangChain agent architecture."""
    try:
        from langchain.agents import create_agent
        return create_agent(
            model=llm,
            tools=[],
            system_prompt=SYSTEM
        )
    except Exception as e:
        print(f"Agent creation note: {e}")
        return None


if __name__ == "__main__":
    print("--- 1. Multi-Turn Tailoring Assistant (Conversational Memory) ---")
    q1 = "Hi, I'm Veky. Do you stitch suits?"
    print(f"Customer: {q1}")
    try:
        print(f"Assistant: {ask(q1)}\n")
    except Exception as e:
        print(f"Response/API Note: {e}\n")

    q2 = "What's my name?"
    print(f"Customer: {q2}")
    try:
        print(f"Assistant: {ask(q2)}\n")
    except Exception as e:
        print(f"Response/API Note: {e}\n")

    print("--- 2. Autonomous Agent Architecture Test ---")
    agent_order = create_tailoring_agent()
    if agent_order:
        agent_query = "Do you stitch formal shirts?"
        print(f"Customer: {agent_query}")
        try:
            result_order = agent_order.invoke({
                "messages": [
                    {
                        "role": "user",
                        "content": agent_query
                    }
                ]
            })
            print(f"Agent: {result_order['messages'][-1].content}\n")
        except Exception as e:
            print(f"Agent execution note: {e}\n")
