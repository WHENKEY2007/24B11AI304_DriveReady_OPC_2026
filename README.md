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
├── .env.example
├── .gitignore
└── README.md
```

---

## 📅 Workshop Modules

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

---

## ⚙️ Setup & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/WHENKEY2007/24B11AI304_DriveReady_OPC_2026.git
   cd 24B11AI304_DriveReady_OPC_2026
   ```

2. **Install dependencies:**
   ```bash
   pip install openai langchain-groq groq python-dotenv ipywidgets
   ```

3. **Configure API Key:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Add your Groq API key:
     ```env
     GROQ_API_KEY=gsk_your_key_here
     ```

4. **Run any day's task:**
   ```bash
   python Day-1/task.py
   python Day-2/task.py
   python Day-3/task.py
   ```
