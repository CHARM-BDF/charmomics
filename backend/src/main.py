import json

from fastapi import (FastAPI, Form)

from langchain.chat_models import init_chat_model

configurable_model = init_chat_model(
    configurable_fields=(
        "model", "model_provider", "base_url", "num_thread"
    )
)

conversationTest = [
    {
        "user": "assistant",
        "message": "My name is Franklin and I will be your assistant, how can I help you today?"
    },
    {
        "user": "developer",
        "message": "Hi Franklin! Can you help me with omics data today?"
    },
    {
        "user": "assistant",
        "message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur vulputate sapien tincidunt, gravida tellus quis, ullamcorper ante. Mauris vel dui sit amet libero imperdiet malesuada. In porttitor erat ut efficitur cursus. Aenean tincidunt elementum lectus eget condimentum. In accumsan id orci at pulvinar. Proin nec pulvinar erat. Vestibulum feugiat dui eu justo rhoncus sagittis. Integer luctus bibendum orci at fringilla. Aliquam tempus felis quis eros mollis, eget eleifend ante mattis. Vestibulum vel urna at dolor tempor laoreet. Nullam metus justo, facilisis sed scelerisque ut, tristique non odio. Maecenas a feugiat mauris, et consectetur leo. Cras ut neque enim. Phasellus non urna venenatis ipsum rhoncus facilisis at at lacus. Etiam ullamcorper molestie est a fermentum. Fusce egestas elit diam, non aliquam nisi cursus at. Quisque purus tellus, placerat eu scelerisque id, hendrerit in augue. Mauris vitae nisl at dolor vehicula tristique. In hac habitasse platea dictumst. Aliquam erat volutpat. In ac commodo nisi, vitae sodales est. Morbi rutrum cursus aliquam. Fusce dictum, nulla non dignissim bibendum, lorem augue pulvinar eros, non porttitor leo lorem et ligula. Cras non ornare sapien. Fusce ut dictum risus, non sollicitudin quam. Curabitur id diam eget quam tempus fermentum. Phasellus in magna quam. In scelerisque orci placerat ligula pellentesque, fermentum mollis mauris porta. Vestibulum facilisis eros tempor, posuere neque venenatis, mattis justo. Quisque vitae est feugiat, maximus nunc in, vestibulum lectus."
    },
]

conversation = [
    {
        "user": "assistant",
        "message": "My name is Franklin and I will be your assistant, how can I help you today?"
    },
]

# FastAPI Setup
app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello World" }

@app.post("/query")
async def query(
    user: str = Form(...),
    message: str = Form(...)
):
    userMessage = {
        "user": user,
        "message": message
    }

    conversation.append(userMessage)

    response = configurable_model.invoke(
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

    assistantMessage = {
        "user": "assistant",
        "message": response.content
    }

    conversation.append(assistantMessage)

    return assistantMessage

@app.get("/conversation")
def currentConveration():
    return conversation
