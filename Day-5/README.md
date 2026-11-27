# 🧵 Day 5: Retrieval-Augmented Generation (RAG) & State Checkpointing

## 📌 Overview
Day 5 introduces **Retrieval-Augmented Generation (RAG)**, **vector databases**, and **stateful multi-session thread checkpointing** to the **Balu Tailors** workshop agent. We index curated domain knowledge into **ChromaDB** using **HuggingFace dense embeddings**, expose knowledge retrieval as a native LangChain tool alongside transactional database tools, enforce strict grounding and hallucination guardrails, and manage isolated customer conversation threads via **LangGraph's `InMemorySaver`**.

---

## 🎯 Key Concepts Covered

1. **Domain Knowledge Base Curation & Chunking:**
   - Defining 15 precise business facts for Balu Tailors covering offered services (kurti, chudidar, pant stitching, alterations, custom neck/sleeve styling, fabric policies).
   - Encapsulating facts into discrete LangChain `Document` chunks annotated with metadata (`fact_number`, `business`).

2. **Vector Embeddings & ChromaDB Indexing:**
   - Generating semantic dense vectors with `sentence-transformers/all-MiniLM-L6-v2` via `HuggingFaceEmbeddings`.
   - Creating and querying a local vector store collection (`balu_tailors_knowledge`) in **ChromaDB**.

3. **Knowledge Retrieval as a First-Class Tool:**
   - Exposing similarity search via the `@tool` decorator (`search_business_knowledge`).
   - Equipping the agent to autonomously decide when to query static business facts versus when to call live calculation or database tools.

4. **Unified Multi-Tool Agent with Strict Grounding Guardrails:**
   - Combining live business tools (`get_price`, `find_customer`, `log_order`) with RAG retrieval (`search_business_knowledge`).
   - Enforcing strict system boundaries:
     - Use retrieved facts as evidence; admit unknowns (*"I don't have that information. Please confirm with Balu Tailors."*).
     - Explicitly reject unoffered services (e.g. blouse stitching/alterations).
     - Direct all pricing queries to `get_price` rather than general estimates.

5. **Session Management & Thread Isolation with LangGraph Checkpointer:**
   - Attaching `InMemorySaver` checkpointing to `create_agent`.
   - Managing multi-user dialogue state using `thread_id` configurations (`customer_A`, `customer_B`).
   - Preventing cross-session context bleeding and verifying customer conversational privacy.

6. **Automated Verification & Boundary Testing:**
   - Validating agent responses across known facts, ungrounded inquiries, negative constraints, and verifying thread-isolated recall.

---

## 🚀 How to Run

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/WHENKEY2007/24B11AI304_DriveReady_OPC_2026/blob/main/Day-5/task.py)

### Prerequisites & Execution:
1. **Install dependencies:**
   ```bash
   pip install langchain langchain-groq gspread pydantic langchain-chroma langchain-huggingface sentence-transformers langgraph python-dotenv
   ```

2. **Configure API Key:**
   - Ensure your Groq API key is present in `.env`:
     ```env
     GROQ_API_KEY=gsk_your_groq_key_here
     ```

3. **Run the task:**
   ```bash
   python Day-5/task.py
   ```
