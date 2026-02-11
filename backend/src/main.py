""" Entry points for the CHARMomics backend """
import logging
import logging.config

from os import path
from fastapi import FastAPI

from src.routers import annotation_router, diagnostics_router

# create logger
log_file_path = path.join(path.dirname(path.abspath(__file__)), '../logging.conf')
logging.config.fileConfig(log_file_path, disable_existing_loggers=False)

logger = logging.getLogger(__name__)

# FastAPI Setup
app = FastAPI(root_path="/charmomics/api/")

app.include_router(annotation_router.router)
app.include_router(diagnostics_router.router)

### FastAPI Routes ###


@app.get("/heart-beat", tags=["lifecycle"])
def heartbeat():
    """Returns a heart-beat that orchestration services can use to determine if the application is running"""

    return "thump-thump"
