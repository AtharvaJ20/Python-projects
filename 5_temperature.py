import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import asyncio
import sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()
key = os.environ["GEMINI_API_KEY"]

SYSTEM_PROMPT = ("You are a tagline specialist. Give me a suitable tagline for the prompt i am giving." 
"Reply in 5 words.")


async def generate(prompt,temperature):
    try:
        client = genai.Client()
        response = await client.aio.models.generate_content(
            model = "gemini-3.5-flash-lite",
            contents = prompt,
            config = types.GenerateContentConfig(
                system_instruction = SYSTEM_PROMPT,
                temperature = temperature
            )
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error : {e}")
        return None

async def main():
    prompt = "Give me a tagline for a chai shop in 5 words."

    low = await asyncio.gather(*[generate(prompt,0) for _ in range(5)])
    high = await asyncio.gather(*[generate(prompt,1.5) for _ in range(5)])

    print("Temperature : 0")
    for r in low:
        print(" ",r)
    #print("unique answers:", len(set(low)))
    print(Counter(low).most_common())

    print("temperature : 1.5")
    for r in high:
        print(" ",r)
    #print("Unique answers:", len(set(high)))
    print(Counter(high).most_common())

asyncio.run(main())

    