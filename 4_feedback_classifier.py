import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import asyncio
import sys

sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

key = os.environ["GEMINI_API_KEY"]

SYSTEM_PROMPT = (
    "You are a review analyst. Classify the sentiment of the feedback "
    "you are given. Reply with exactly one word: "
    "positive, negative, neutral or mixed."
)
ALLOWED = {"positive", "negative", "neutral", "mixed"}

async def classify_feedback(feedback):
    try:
        client = genai.Client()
        response = await client.aio.models.generate_content(
            model = "gemini-3.5-flash-lite",
            contents = feedback,
            config = types.GenerateContentConfig(
                system_instruction=(SYSTEM_PROMPT),
            )
        )
        label = response.text.strip().lower()
        if label not in ALLOWED:
            return None
        return label
        
    except Exception as e:
        print(f"Error : {e}")
        return None

async def main():
    feedbacks = [
        "Loved the packaging, will buy again!",
        "Delivery took 9 days and the box was damaged.",
        "It works.",
        "Great phone but the battery dies by noon."
    ]

    
    tasks = [classify_feedback(f) for f in feedbacks]
    results = await asyncio.gather(*tasks)
    for f, r in zip(feedbacks,results):
        print(f"{f!r:50} -> {r}")

    failed = results.count(None)
    print(f"Batch finished: {len(results)-failed} ok, {failed} failed")

asyncio.run(main())

