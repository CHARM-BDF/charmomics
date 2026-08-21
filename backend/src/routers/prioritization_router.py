"""  """

import logging
import json 

from typing import Annotated
from pathlib import Path
from queue import Queue

from fastapi import APIRouter, Depends, File

from src.dependencies import database
from src.core.pipeline import PipelineService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/prioritization", tags=["prioritization"], dependencies=[Depends(database)])

@router.post("/")
def variant_prioritization(
    sample: str,
    vcf_file: Annotated[bytes, File()]
):
    """  """

    vcf_sample_path = Path(f"./etc/data/raw/{sample}/{sample}.vcf")

    vcf_sample_path.parent.mkdir(parents=True, exist_ok=True)

    with open(vcf_sample_path, "wb") as file:
        file.write(vcf_file)

    queue = Queue()

    pipeline_json = json.load(open('./etc/pipeline.json'))

    pipeline = PipelineService(queue)
    pipeline.queue_pipeline_tasks(pipeline_json)
    pipeline.process_tasks()

    return "Hello World"
