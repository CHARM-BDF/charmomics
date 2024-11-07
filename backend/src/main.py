from fastapi import FastAPI



message = [
    ("human", "Hello"),
]

# FastAPI Setup
app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Hello World" }

@app.get("/query")
async def query():

    return { "message": "Message!" }
