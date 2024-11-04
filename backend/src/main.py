from fastapi import FastAPI

app = FastAPI(root_path="/api/")

@app.get("/")
async def root():
    """ Prototype greeting """

    return {"message": "Hello World"}
