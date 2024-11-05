from fastapi import FastAPI

from langchain_ollama.chat_models import ChatOllama

chain = ChatOllama(
    model="llama3.2",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    base_url="http://138.26.49.205:11435",
)

message = [
    ("human", "Hello"),
]

# FastAPI Setup

app = FastAPI(root_path="/api/")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/query")
async def query():
    return chain.invoke(message)
