# ✂️ Day 3: Conversational Memory, Automated Evaluation & LangChain Agents

## 📌 Overview
Day 3 focuses on building specialized conversational assistants and agent workflows using **LangChain** and **Google Gemini** (`ChatGoogleGenerativeAI`). Key topics include structured prompt engineering with strict behavioral boundaries, multi-turn stateful conversational memory using `MessagesPlaceholder`, automated benchmark testing and compliance evaluation, and transitioning to autonomous agent architectures using `create_agent`.

---

## 🎯 Key Concepts Covered

1. **Google Gemini Integration via LangChain:**
   - Initializing `ChatGoogleGenerativeAI` from `langchain-google-genai` using Gemini models (e.g., `gemini-3.8-flash` / `gemini-1.5-flash`).
   - Secure credential management using `google.colab.userdata` and environment variables (`GOOGLE_API_KEY`).
   - Setting sampling temperature (`temperature=0.2`) for consistent, rule-compliant responses.

2. **Domain-Specific Persona & Behavioral Guardrails (Men's Tailoring Assistant):**
   - **Role:** Specialized tailoring assistant for custom men's garments and alterations.
   - **Facts:** Catalog of services (shirt, pant, trouser, suit, blazer, kurta stitching, and alterations); explicitly requiring custom measurements and stating pricing dependencies (garment type, fabric, design).
   - **Rules:** Guardrails against hallucinations—never inventing prices or promising delivery dates/locations; utilizing explicit fallbacks (*"I'll check with the tailor."*); requiring garment and design details before discussing pricing.
   - **Format Constraints:** Strict response length limit (under 50 words), multi-lingual adaptability (responding in simple English or Telugu matching customer language), and polite conversational tone.

3. **Multi-Turn Conversational Memory with LCEL:**
   - Composing prompt templates using `ChatPromptTemplate.from_messages` with `MessagesPlaceholder("history")`.
   - Streaming and chaining with LangChain Expression Language (`prompt | llm | StrOutputParser()`).
   - Maintaining and updating multi-turn chat history (`history.extend([("human", question), ("ai", answer)])`).

4. **Automated Evaluation & Rule Compliance Testing:**
   - Implementing automated test suites (`run_tests`) that read test cases from evaluation datasets (`test.csv`).
   - Programmatically asserting required keyphrases and behavioral compliance (`must_include`) across test queries to verify agent reliability and measure pass rates.

5. **Agent Architecture with `create_agent`:**
   - Setting up autonomous agents using `langchain.agents.create_agent` (leveraging LangGraph execution).
   - Supplying system instructions, toolsets, and managing structured message state for scalable agentic workflows.

---

## 🚀 How to Run

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/WHENKEY2007/24B11AI304_DriveReady_OPC_2026/blob/main/Day-3/task.py)

### Prerequisites & Execution:
1. **Install dependencies:**
   ```bash
   pip install langchain-google-genai langchain-core langchain
   ```

2. **Configure API Key:**
   - Set the `GOOGLE_API_KEY` environment variable:
     ```bash
     export GOOGLE_API_KEY="your_api_key_here"
     ```
   - In Google Colab, add `GOOGLE_API_KEY` under the Secrets tab.

3. **Run the notebook / task:**
   - Open directly in Google Colab using the badge above or run in your Jupyter / Python environment.
