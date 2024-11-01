import os
import taipy.gui.builder as tgb

from dotenv import find_dotenv, load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_ollama.chat_models import ChatOllama
from langchain.chains import GraphCypherQAChain
from langfuse.callback import CallbackHandler
from taipy.gui import Gui, notify

from langchain_openai import ChatOpenAI

# Load environment variables from file
env_file = find_dotenv("/app/.env")
load_dotenv(env_file)

graph = Neo4jGraph()

langfuse_handler = CallbackHandler(
    public_key=os.getenv("PUBLIC_KEY"),
    secret_key=os.getenv("SECRET_KEY"),
    host=os.getenv("HOST"),
)

chain = GraphCypherQAChain.from_llm(
    ChatOllama(
        model="llama3.1:70b",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # api_key= os.getenv("OPENAI_API_KEY"),
        base_url="http://138.26.49.202:11435",
        # organization="...",
        # other params...
    ),
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True
)


def query_llm(query_message):
    return chain.invoke(query_message, callbacks=[langfuse_handler])


query_message = ""
messages = []
messages_dict = {}


def on_init(state):
    state.messages = [
        {
            "style": "assistant_message",
            "content": "Hello, my name is Franklin! How can I help you today?",
        },
    ]
    new_conv = create_conv(state)
    state.conv.update_content(state, new_conv)


def create_conv(state):
    messages_dict = {}
    with tgb.Page() as conversation:
        for i, message in enumerate(state.messages):
            text = message["content"].replace("<br>", "\n").replace('"', "'")
            messages_dict[f"message_{i}"] = text
            tgb.text(
                f"{{messages_dict.get('message_{i}') or ''}}",
                class_name=f"message_base {message['style']}",
                mode="md",
            )
    state.messages_dict = messages_dict
    return conversation


def send_message(state):
    state.messages.append(
        {
            "style": "user_message",
            "content": state.query_message,
        }
    )
    state.conv.update_content(state, create_conv(state))
    notify(state, "info", "Sending message...")
    state.messages.append(
        {
            "style": "assistant_message",
            "content": query_llm(state.query_message),
        }
    )
    state.conv.update_content(state, create_conv(state))
    state.query_message = ""


def reset_chat(state):
    state.query_message = ""
    on_init(state)


with tgb.Page() as page:
    with tgb.layout(columns="350px 1"):
        with tgb.part(class_name="sidebar"):
            tgb.text("## Franklin", mode="md")
            tgb.button(
                "New Conversation",
                class_name="fullwidth plain",
                on_action=reset_chat,
            )
            # tgb.table("{pdf_names}", show_all=True)

        with tgb.part(class_name="p1"):
            tgb.part(partial="{conv}", height="600px", class_name="card card_chat")
            with tgb.part("card mt1"):
                tgb.input(
                    "{query_message}",
                    on_action=send_message,
                    change_delay=-1,
                    label="Write your message:",
                    class_name="fullwidth",
                )

if __name__ == "__main__":
    gui = Gui(page)
    conv = gui.add_partial("")
    gui.run(title="Franklin", dark_mode=False, margin="0px", debug=True, base_url="/chatbot")
