from fastapi import FastAPI
from pydantic import BaseModel
from app.ollama_client import ask_ollama
from app.openai_client import ask_openai
import time
from app.neo4j_client import test_connection, store_user_chat, driver

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

    if ollama_resp:
        # Extract string if response is dict
        resp_text = ollama_resp["response"] if isinstance(ollama_resp, dict) else ollama_resp
        store_user_chat("user1", request.message, resp_text)

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

    if ollama_resp:  # only store if response exists
     store_user_chat("user1", request.message, ollama_resp)

    

@app.get("/test-neo4j")
def test_neo4j():
    message = test_connection()
    return {"message": message}

@app.get("/get-chats")
def get_chats():
    with driver.session() as session:
        result = session.run("""
        MATCH (u:User)-[:SENT]->(c:Chat)
        RETURN u.id AS user, c.message AS message, c.response AS response
        """)

        data = []
        for record in result:
            data.append(record.data())

        return data