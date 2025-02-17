from fastapi import APIRouter, Form

from langchain.chat_models import init_chat_model

router = APIRouter(prefix="/assistant", tags=['assistant'])

configurable_model = init_chat_model(configurable_fields=("model", "model_provider", "base_url", "num_thread"))

conversation = [{
    "user": "assistant", "message": "I am CHARMomics and can be your assistant, how can I help you today?"
}, {"user": "developer", "message": "Hello!"}]


@router.post("/query")
async def query(user: str = Form(...), message: str = Form(...)):
    """ The prompt the user sends to the large language model """

    user_message = {"user": user, "message": message}

    conversation.append(user_message)

    response = configurable_model.invoke(
        input=message,
        config={
            "configurable": {
                "model": "llama3.2", "model_provider": "ollama", "temperature": 0, "max_tokens": None, "timeout": None,
                "max_retries": 2, "num_thread": 16, "base_url": "http://138.26.49.205:11435"
            }
        }
    )

    assistant_message = {"user": "assistant", "message": response.content}

    conversation.append(assistant_message)

    return assistant_message


@router.get("/conversation")
def current_converation():
    """ Returns the existing conversation with the model and the user """

    return conversation
