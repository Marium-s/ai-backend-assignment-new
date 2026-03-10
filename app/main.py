from fastapi import FastAPI
from pydantic import BaseModel

import time
from app.neo4j_client import test_connection, store_user_chat, driver

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "FastAPI server running"}   
  

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