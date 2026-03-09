import time
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file

OPENAI_API_KEY = os.getenv("OpenAi_key")

client = OpenAI(api_key="OPENAI_API_KEY")

def ask_openai(prompt: str):
    start = time.time()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    end = time.time()

    return {
        "response": response.choices[0].message.content,
        "latency": round(end - start, 2)
    }