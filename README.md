# 🤖 24B11AI304_DriveReady_OPC_2026 — Agentic AI Workshop

This repository contains the practical assignments and code developed during the **DriveReady Agentic AI Workshop (OPC 2026)**.

---

## 📁 Repository Structure

```text
24B11AI304_DriveReady_OPC_2026/
├── Day-1/
│   ├── task.py             # LangChain + Groq Assistant with Prompt Guard
│   └── README.md           # Day 1 learnings and documentation
├── Day-2/
│   ├── task.py             # HealthTrack AI Agent with Memory & Tool Tracking
│   └── README.md           # Day 2 learnings and documentation
├── Day-3/
│   ├── task.py             # Tailoring Assistant with Memory, Evaluation & Agent Workflows
│   └── README.md           # Day 3 learnings and documentation
├── Day-4/
│   ├── task.py             # Tool Use, Structured Outputs & Execution Tracing
│   └── README.md           # Day 4 learnings and documentation
├── Day-5/
│   ├── task.py             # RAG Knowledge Retrieval, ChromaDB & Thread Checkpointing
│   └── README.md           # Day 5 learnings and documentation
├── .env.example
├── .gitignore
└── README.md
```

---

## 📅 Workshop Modules

| Day | Topic / Focus | Frameworks & Models | Key Concepts & Deliverables | Code |
| :--- | :--- | :--- | :--- | :--- |
| **[Day 1](Day-1/README.md)** | Foundations & Prompt Guardrails | LangChain, Groq Cloud, `openai/gpt-oss-120b`, `llama-prompt-guard-2-22m` | • Sweet Crumbs Bakery persona design<br>• Behavioral rules & formatting limits<br>• Llama Prompt Guard security defense | [`Day-1/task.py`](Day-1/task.py) |
| **[Day 2](Day-2/README.md)** | Multi-Turn HealthTrack AI Agent | OpenAI SDK, Groq Cloud, `openai/gpt-oss-120b` | • Stateful `HealthTrackAgent` class<br>• Sliding-window conversational memory<br>• Intent routing & JSON entity extraction<br>• API error handling & `@log_call` decorator | [`Day-2/task.py`](Day-2/task.py) |
| **[Day 3](Day-3/README.md)** | Conversational Memory & Agent Workflows | LangChain, Google GenAI, `gemini-1.5-flash`, LangGraph | • Men's Tailoring Assistant (bilingual)<br>• LCEL chain with `MessagesPlaceholder`<br>• Automated benchmark suite (`test.csv`)<br>• Autonomous agent via `create_agent` | [`Day-3/task.py`](Day-3/task.py) |
| **[Day 4](Day-4/README.md)** | Tool Calling, Structured Outputs & Tracing | LangChain, Groq Cloud, `openai/gpt-oss-20b`, Pydantic, gspread | • Pydantic `TailoringOrder` schema validation<br>• Structured output parsing from messy text<br>• Google Sheets integration & `@tool` decorators<br>• Tool description sensitivity & trace count metrics | [`Day-4/task.py`](Day-4/task.py) |
| **[Day 5](Day-5/README.md)** | RAG, ChromaDB & State Checkpointing | LangChain, Groq Cloud, `openai/gpt-oss-20b`, ChromaDB, HuggingFace, LangGraph | • 15 business facts chunked into Chroma vector store<br>• Dense embeddings (`all-MiniLM-L6-v2`)<br>• RAG retrieval tool (`search_business_knowledge`)<br>• LangGraph `InMemorySaver` thread isolation | [`Day-5/task.py`](Day-5/task.py) |

---

### [Day 1: Foundations & Prompt Guardrails](Day-1/README.md)
- High-speed inference using Groq LPU and LangChain.
- System prompt design with persona, facts, behavioral rules, and formatting limits.
- Prompt injection defense using Meta's `llama-prompt-guard-2-22m`.

### [Day 2: HealthTrack AI Multi-Turn Agent](Day-2/README.md)
- Custom agent class with sliding-window conversational memory.
- Dynamic intent classification (`health_question`, `habit_tracking`, etc.).
- Strict JSON entity extraction and user health state updates.
- API error handling (`RateLimitError`, `APIConnectionError`).
- Observability and logging using Python decorators (`@log_call`).

### [Day 3: Conversational Memory, Automated Evaluation & LangChain Agents](Day-3/README.md)
- Multi-turn conversation chains using LangChain and Google Gemini (`ChatGoogleGenerativeAI`).
- Specialized persona engineering with strict domain facts, behavioral boundaries, and bilingual rules.
- Stateful conversational memory using `MessagesPlaceholder`.
- Benchmark evaluation suite for automated compliance and regression testing (`test.csv`).
- Autonomous agent workflows initialized with `create_agent`.

### [Day 4: Tool Calling, Structured Outputs & Agent Tracing](Day-4/README.md)
- Schema-driven order validation using Pydantic models (`TailoringOrder`).
- Unstructured entity extraction from messy customer messages via `llm.with_structured_output`.
- Business tool integration (`get_price`, `find_customer`, `log_order`) with Google Sheets persistence.
- Tool description sensitivity testing (evaluating clear vs ambiguous docstrings on agent behavior).
- Programmatic call tracing and observability (counting model calls, tool calls, and results).

### [Day 5: Retrieval-Augmented Generation (RAG) & State Checkpointing](Day-5/README.md)
- Domain knowledge base indexing into ChromaDB using HuggingFace dense embeddings (`all-MiniLM-L6-v2`).
- Knowledge retrieval exposed as an autonomous agent tool (`search_business_knowledge`).
- Multi-tool orchestration combining live database/sheet operations with factual grounding.
- Multi-user conversational isolation using LangGraph thread checkpointing (`InMemorySaver`).

---

## ⚙️ Setup & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/WHENKEY2007/24B11AI304_DriveReady_OPC_2026.git
   cd 24B11AI304_DriveReady_OPC_2026
   ```

2. **Install dependencies:**
   ```bash
   pip install openai langchain-groq groq langchain-google-genai langchain-core langchain gspread pydantic langchain-chroma langchain-huggingface sentence-transformers langgraph python-dotenv
   ```

3. **Configure API Keys:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Add your API keys:
     ```env
     GROQ_API_KEY=gsk_your_groq_key_here
     GOOGLE_API_KEY=AIzaSy_your_google_key_here
     ```

4. **Run any day's task:**
   ```bash
   python Day-1/task.py
   python Day-2/task.py
   python Day-3/task.py
   python Day-4/task.py
   python Day-5/task.py
   ```
