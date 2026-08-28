"""  """

import logging
import json 

from typing import Annotated
from pathlib import Path
from queue import Queue

from fastapi import APIRouter, Depends, File, UploadFile

from src.dependencies import database
from src.core.pipeline import PipelineService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/prioritization", tags=["prioritization"], dependencies=[Depends(database)])

@router.post("/")
def variant_prioritization(
    sample: str,
    # vcf_file: Annotated[bytes, File()]
    vcf_file: UploadFile
):
    """  """

    raw_path = Path(f"./etc/data/raw/{sample}/")
    interim_path = Path(f"./etc/data/interim/{sample}/")
    results_path = Path(f"./etc/data/result/{sample}/")

    raw_path.mkdir(parents=True, exist_ok=True)
    interim_path.mkdir(parents=True, exist_ok=True)
    results_path.mkdir(parents=True, exist_ok=True)

    vcf_sample_file = Path(f"{raw_path}/{vcf_file.filename}")

    attributes = {
        'sample': sample,
        'file_name': vcf_file.filename,
        'raw_path': raw_path,
        'interim_path': interim_path,
        'results_path': results_path
    }

    print(vcf_sample_file)

    with open(vcf_sample_file, "wb") as file:
        file.write(vcf_file.file.read())

    queue = Queue()

    pipeline_json = json.load(open('./etc/pipeline.json'))
    
    pipeline = PipelineService(queue)
    pipeline.queue_pipeline_tasks(pipeline_json, attributes)
    pipeline.process_tasks()

    return "Done!"
