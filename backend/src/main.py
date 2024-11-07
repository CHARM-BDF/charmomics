from fastapi import (FastAPI, Form)

from langchain.chat_models import init_chat_model

configurable_model = init_chat_model(
    configurable_fields=(
        "model", "model_provider", "base_url", "num_thread"
    )
)

message = [
    ("human", "Hello"),
]

# FastAPI Setup
app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello World" }

@app.post("/query")
async def query(
    sender: str = Form(...),
    message: str = Form(...)
):
    return configurable_model.invoke(
        input = message,
        config={
            "configurable": {
                "model": "llama3.2",
                "model_provider": "ollama",
                "temperature": 0,
                "max_tokens": None,
                "timeout": None,
                "max_retries": 2,
                "num_thread": 16,
                "base_url": "http://138.26.49.205:11435"
            }
        }
    )
