import os
from google import genai
from dotenv import load_dotenv
import sys

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

key = os.environ["GEMINI_API_KEY"]


def ask_gemini(prompt):
    try:
        client = genai.Client()
        
        response = client.models.generate_content(
            model = "gemini-3.5-flash-lite",
            contents = prompt,
            )
        print(response.usage_metadata)
        return response.text
    except Exception as e:
        print(f"Error:{e}")
    finally:
        print("Call finished")

print(ask_gemini("Explain what token is in one sentence"))

