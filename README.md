# 🤖 Agentic AI Workshop — Day 1

Welcome to **Day 1** of the Agentic AI Workshop! This repository covers foundational concepts for building robust, secure, and production-ready LLM-powered agents using **LangChain**, **Groq**, and **Prompt Guard**.

---

## 📚 Key Learnings & Concepts

### 1. Fast LLM Inference with Groq & LangChain
- **Groq LPU Inference:** Utilizing Groq's high-speed Language Processing Units (LPUs) for ultra-low latency completions.
- **LangChain Integration:** Initializing and configuring `ChatGroq` models (`openai/gpt-oss-120b`, Llama 3, etc.) with deterministic temperature settings (`temperature=0`).

### 2. System Prompts, Personas & Guardrails
- **Persona Engineering:** Structuring system prompts into distinct pillars:
  - **Role & Identity:** Defining who the assistant is (e.g., Sweet Crumbs Bakery assistant).
  - **Facts (Knowledge Boundary):** Baking to order, 24-hour advance notice, availability of eggless versions.
  - **Rules (Behavioral Guardrails):** Explicit instructions not to promise delivery times, and admitting when an answer is unknown.
  - **Formatting Constraints:** Restricting output style and length (e.g., polite responses in under 60 words).
- **Context Injection:** Packaging interactions into structured system and human tuples `[("system", SYSTEM), ("human", question)]`.

### 3. LLM Security & Prompt Injection Defense
- **The Threat of Prompt Injections:** How user inputs can attempt to hijack system instructions (e.g., *"Ignore your previous instructions..."*).
- **Llama Prompt Guard (`meta-llama/llama-prompt-guard-2-22m`):** Implementing a dedicated, lightweight safety classifier that inspects incoming user prompts and scores injection/jailbreak probabilities (e.g., outputting a `0.998` confidence score for attack detection) before executing expensive model calls.

### 4. Production Secret & Environment Management
- **Never Hardcode API Keys:** Protecting sensitive credentials (`GROQ_API_KEY`) from Git leaks and automated scraping bots.
- **Multi-Environment Configuration:** Seamlessly supporting local development via `.env` files and `python-dotenv`, while falling back to Google Colab Secrets (`userdata.get`) or interactive prompts (`getpass`).

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd AgenticAI
```

### 2. Install Dependencies
```bash
pip install langchain-groq groq python-dotenv
```

### 3. Set Up Your API Key
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_actual_key_here
   ```
   *(The `.env` file is excluded in `.gitignore` so your key remains safe).*

### 4. Run the Notebook
Open and execute [agenticAI_Day1.ipynb](agenticAI_Day1.ipynb) in your preferred environment (VS Code, Jupyter, or Google Colab).

---

## 📂 Project Structure
```text
AgenticAI/
├── agenticAI_Day1.ipynb   # Day 1 interactive workshop notebook
├── .env.example           # Template for environment variables
├── .gitignore             # Git ignore file protecting .env and build files
└── README.md              # Workshop documentation & key learnings
```
