# 🍰 Day 1: Foundations of Agentic AI & Prompt Guardrails

## 📌 Overview
Day 1 introduces the core building blocks of LLM-based conversational agents using **LangChain** and **Groq Cloud**, focusing on persona design, behavioral guardrails, and prompt injection defense.

---

## 🎯 Key Concepts Covered

1. **High-Speed Inference with Groq:**
   - Setting up `ChatGroq` with `openai/gpt-oss-120b` for low-latency completions.
   - Temperature tuning (`temperature=0`) for deterministic, factual outputs.

2. **Persona Engineering & Guardrails:**
   - **Role:** Defining clear identity (Sweet Crumbs Home Bakery assistant).
   - **Facts:** Knowledge boundaries (bake to order, 24-hr advance notice, eggless versions available).
   - **Rules:** Behavioral restrictions (never promise delivery times, admit unknowns).
   - **Format:** Output constraints (polite tone, under 60 words).

3. **LLM Security with Llama Prompt Guard:**
   - Classifying input prompts with `meta-llama/llama-prompt-guard-2-22m`.
   - Detecting jailbreak and prompt injection attempts before they reach the main agent.

4. **Production Secret Management:**
   - Safe API key handling using `.env` and `python-dotenv`.

---

## 🚀 How to Run

```bash
python Day-1/task.py
```
