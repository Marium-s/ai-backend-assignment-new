from fastapi import FastAPI
from pydantic import BaseModel
from app.ollama_client import ask_ollama
from app.openai_client import ask_openai
import time

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "FastAPI server running"}

@app.post("/chat")
def chat(request: ChatRequest):
    # Ollama response
    start_ollama = time.time()
    try:
        ollama_resp = ask_ollama(request.message)
        ollama_latency = time.time() - start_ollama
    except Exception as e:
        ollama_resp = None
        ollama_latency = None
        ollama_error = str(e)

    # OpenAI response
    start_openai = time.time()
    try:
        openai_resp = ask_openai(request.message)
        openai_latency = time.time() - start_openai
        openai_error = None
    except Exception as e:
        openai_resp = None
        openai_latency = None
        openai_error = str(e)


    return {
        "ollama": {
            "response": ollama_resp,
            "latency": ollama_latency,
            "error": ollama_error if 'ollama_error' in locals() else None
        },
        "openai": {
            "response": openai_resp,
            "latency": openai_latency,
            "error": openai_error
        }
    }
