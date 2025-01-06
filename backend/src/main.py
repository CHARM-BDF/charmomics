""" Entry points for the Franklin backend """
import logging
import logging.config

from os import path
from fastapi import FastAPI

from src.routers import annotation_router, assistant_router

# create logger
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

# FastAPI Setup
app = FastAPI(root_path="/api/")

app.include_router(annotation_router.router)
app.include_router(assistant_router.router)

### FastAPI Routes ###


@app.get("/")
async def root():
    """ Root endpoint to ensure Franklin is working """

    return {"message": "Hello World"}
