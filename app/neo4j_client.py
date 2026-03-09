import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Create driver
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def test_connection():
    try:
        driver.verify_connectivity()
        return "Neo4j connection successful!"
    except Exception as e:
        return f"Error: {str(e)}"


def store_user_chat(user_id: str, message: str, response: str):
    try:
        with driver.session() as session:
            session.run(
                """
                MERGE (u:User {id: $user_id})
                CREATE (c:Chat {message: $message, response: $response})
                MERGE (u)-[:SENT]->(c)
                """,
                user_id=user_id,
                message=message,
                response=response
            )
        return "Chat stored successfully"
    except Exception as e:
        return f"Error storing chat: {str(e)}"