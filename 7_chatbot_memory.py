import os
from google import genai
from google.genai import types
import asyncio
from dotenv import load_dotenv
import sys

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()
key = os.environ["GEMINI_API_KEY"]

client = genai.Client()
history = []

def chat(user_message):
    history.append({"role":"user", "parts":[{'text':user_message}]})

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=history[-6:],
        )
        reply = response.text
        history.append({"role":"model", "parts":[{"text":reply}]})
        return reply

    except Exception as e:
        print(f"Error: {e}")
        history.pop()
        return None

def main():
    while True:
        text = input("You: ")
        if text == 'quit':
            break
        print("Bot:",chat(text))

main()

