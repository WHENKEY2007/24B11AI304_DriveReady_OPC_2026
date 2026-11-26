# 🪡 Day 4: Tool Calling, Structured Outputs & Agent Tracing

## 📌 Overview
Day 4 focuses on advancing agent capabilities through **tool use**, **structured schema extraction**, **external persistence (Google Sheets)**, and **execution trace analysis**. Using the **Balu Tailors** business scenario, we build custom business tools, test the impact of semantic tool descriptions on LLM decision-making, extract strict Pydantic records from unstructured text, and measure model/tool invocation counts.

---

## 🎯 Key Concepts Covered

1. **Structured Data Validation with Pydantic (`TailoringOrder`):**
   - Defining a strict schema for order records matching relational database/sheet structures.
   - Enforcing typing, default values, and literal constraints (`status`, `cutting_status`, `stitching_status`, `price`, `measurements`).

2. **Entity Extraction from Messy Customer Inputs:**
   - Leveraging `llm.with_structured_output(TailoringOrder)` with Groq (`openai/gpt-oss-20b`).
   - Parsing complex, informal customer queries containing garment details, measurements, advance payments, and paired sets into validated Pydantic instances.

3. **Custom Business Tools & Google Sheets Integration:**
   - Wrapping core business functions using LangChain's `@tool` decorator:
     - `get_price`: Queries base garment pricing (`shirt`, `pant`, `pair`, `kurta`, `blouse`, `safari`).
     - `find_customer`: Searches existing customer directories by ID, name, or phone number.
     - `log_order`: Validates order records and writes rows directly to Google Sheets via `gspread`.

4. **Tool Description Engineering & Agent Sensitivity:**
   - Experimenting with agent tool selection by replacing a descriptive tool with an ambiguous counterpart (`tool1` with docstring `"""does stuff"""`).
   - Demonstrating how the LLM relies heavily on docstrings, argument types, and descriptions to select and parameterize appropriate tools.

5. **Execution Tracing & Call Observability:**
   - Inspecting intermediate conversation messages (`AIMessage`, `ToolMessage`).
   - Programmatically analyzing execution traces to count:
     - **Model calls (AI messages):** Total LLM reasoning passes.
     - **Tool calls requested:** Function calls dispatched by the model.
     - **Tool results returned:** Successful executions fed back into the context.

---

## 🚀 How to Run

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/WHENKEY2007/24B11AI304_DriveReady_OPC_2026/blob/main/Day-4/task.py)

### Prerequisites & Execution:
1. **Install dependencies:**
   ```bash
   pip install langchain langchain-groq gspread pydantic python-dotenv
   ```

2. **Configure API Key:**
   - Add your Groq API key to `.env`:
     ```env
     GROQ_API_KEY=gsk_your_groq_key_here
     ```

3. **Run the task:**
   ```bash
   python Day-4/task.py
   ```
