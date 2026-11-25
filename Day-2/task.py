import os
import json
import getpass
from dotenv import load_dotenv
from openai import OpenAI, RateLimitError, APIConnectionError, AuthenticationError

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    try:
        from google.colab import userdata
        GROQ_API_KEY = userdata.get("GROQ_API_KEY")
    except Exception:
        GROQ_API_KEY = getpass.getpass("Enter your Groq API key: ")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "openai/gpt-oss-120b"

SYSTEM_PROMPT = """
You are HealthTrack AI, a friendly personal health assistant.

ROLE:
Help users organize basic health information
and understand general wellness concepts.

FACTS:
- Encourage healthy sleep habits.
- Encourage regular physical activity.
- Encourage balanced nutrition.
- Remind users to follow professional medical advice.

RULES:
- Never diagnose diseases.
- Never prescribe medicines or dosages.
- Never recommend stopping prescribed medication.
- For serious or emergency symptoms, advise seeking
  immediate professional medical assistance.
- Do not invent medical information.
- Ask for clarification when necessary.

FORMAT:
- Use simple English.
- Give short and understandable answers.
- Use bullet points when helpful.
"""

# Global health state
health_data = {
    "sleep_hours": 0,
    "water_glasses": 0,
    "exercise_minutes": 0
}


def classify_intent(user_message: str) -> str:
    """Classify user message into: health_question, habit_tracking, reminder, health_summary."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
                Classify the user's message into exactly one category:
                health_question, habit_tracking, reminder, health_summary.

                Return only the category name.
                """
            },
            {"role": "user", "content": user_message}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()


def extract_health_data(user_message: str) -> dict:
    """Extract structured health entities from free-form user message."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": """
                Extract only information explicitly mentioned by the user.

                Return valid JSON with these fields:
                {
                    "sleep_hours": null,
                    "water_glasses": null,
                    "exercise_minutes": null
                }

                Use null if information is not mentioned.
                Do not guess values.
                """
            },
            {"role": "user", "content": user_message}
        ],
        temperature=0
    )
    return json.loads(response.choices[0].message.content)


def update_health_data(new_data: dict) -> dict:
    """Update user health tracking state."""
    for key, value in new_data.items():
        if value is not None:
            health_data[key] = value
    return health_data


def log_call(func):
    """Decorator to log function execution."""
    def wrapper(*args, **kwargs):
        print(f"Executing: {func.__name__}")
        result = func(*args, **kwargs)
        print("Execution completed!")
        return result
    return wrapper


@log_call
def calculate_weekly_sleep(daily_sleep: list) -> float:
    return sum(daily_sleep) / len(daily_sleep)


class HealthTrackAgent:
    """Multi-turn HealthTrack AI Agent with conversational memory and intent handling."""
    def __init__(self, max_turns=5):
        self.history = []
        self.max_turns = max_turns

    def chat(self, user_message: str) -> str:
        try:
            intent = classify_intent(user_message)

            if intent == "habit_tracking":
                extracted_data = extract_health_data(user_message)
                update_health_data(extracted_data)

            self.history.append({"role": "user", "content": user_message})

            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            messages.extend(self.history[-self.max_turns * 2:])

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.3
            )

            answer = response.choices[0].message.content
            self.history.append({"role": "assistant", "content": answer})
            return answer

        except RateLimitError:
            return "API rate limit reached. Please try again later."
        except APIConnectionError:
            return "Connection problem. Please check your internet."
        except AuthenticationError:
            return "API key authentication failed."
        except Exception as e:
            return f"An error occurred: {e}"


if __name__ == "__main__":
    print("HealthTrack AI connected successfully!\n")
    agent = HealthTrackAgent()

    print("--- 1. Habit Tracking & Entity Extraction ---")
    print("User: I slept for 7 hours and exercised for 30 minutes.")
    print(f"Agent: {agent.chat('I slept for 7 hours and exercised for 30 minutes.')}\n")
    print(f"Current Health Data State: {health_data}\n")

    print("--- 2. Conversational Memory Test ---")
    print("User: My name is Sri Venkatesh.")
    print(f"Agent: {agent.chat('My name is Sri Venkatesh.')}\n")

    print("User: I am studying Artificial Intelligence.")
    print(f"Agent: {agent.chat('I am studying Artificial Intelligence.')}\n")

    print("User: What is my name and what am I studying?")
    print(f"Agent: {agent.chat('What is my name and what am I studying?')}\n")
