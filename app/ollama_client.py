# app/ollama_client.py
import requests
import time

OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_ollama(prompt: str):
    start = time.time()  # Start timer

    payload = {
        "model": "phi",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    data = response.json()

    end = time.time()  # Stop timer

    return {
        "response": data["response"],       # Text from Ollama
        "latency": round(end - start, 2)   # Time in seconds
    }