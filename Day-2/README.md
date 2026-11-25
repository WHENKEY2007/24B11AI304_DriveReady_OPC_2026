# 🩺 Day 2: Multi-Turn HealthTrack AI Agent

## 📌 Overview
Day 2 covers building a stateful, multi-turn AI health assistant (**HealthTrack AI**) featuring intent classification, structured entity extraction, tool logging decorators, and robust API error handling.

---

## 🎯 Key Concepts Covered

1. **OpenAI SDK with Groq API:**
   - Initializing standard `OpenAI` client pointing to Groq (`base_url="https://api.groq.com/openai/v1"`).

2. **Intent Classification & Routing:**
   - Classifying incoming user prompts into `health_question`, `habit_tracking`, `reminder`, or `health_summary`.
   - Routing requests based on intent to specialized workflows.

3. **Structured Entity Extraction:**
   - Prompting the LLM to extract JSON schemas strictly (`sleep_hours`, `water_glasses`, `exercise_minutes`) without hallucinating missing values (`null`).

4. **Conversational Memory & Sliding Context Window:**
   - Maintaining user dialogue history in an agent class (`HealthTrackAgent`).
   - Implementing a sliding window (`max_turns * 2`) to keep context relevant and stay within token limits.

5. **Error Handling & Decorators:**
   - Graceful recovery from `RateLimitError`, `APIConnectionError`, and `AuthenticationError`.
   - Python decorator (`@log_call`) for tracing and observability.

---

## 🚀 How to Run

```bash
python Day-2/task.py
```
