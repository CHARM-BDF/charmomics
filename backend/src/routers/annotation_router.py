""" Annotation endpoint routes that handle all things annotation within the application """

import logging
import re

from fastapi import APIRouter, Depends

from src.core.annotation import AnnotationService
from src.dependencies import database, annotation_queue
from src.enums import OmicUnitType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/annotation", tags=["annotation"], dependencies=[Depends(database)])


@router.post("/")
def annotate_omic_unit(
    type: OmicUnitType, name: str, repositories=Depends(database), annotation_task_queue=Depends(annotation_queue)
):
    """ Initiates annotations for a given omic unit and returns the results when finished """

    omic_unit = {'unit': name, 'type': type}

    omic_unit_exist = repositories['genomic_unit'].find_genomic_unit(omic_unit)

    if not omic_unit_exist:
        new_genomic_unit = None

        if omic_unit['type'] is OmicUnitType.GENE:
            new_genomic_unit = {"gene_symbol": omic_unit['unit'], "gene": omic_unit['unit'], "annotations": []}
        if omic_unit['type'] is OmicUnitType.HGVS_VARIANT:
            new_genomic_unit = {"hgvs_variant": omic_unit['unit'], 'transcripts': [], 'annotations': []}

        repositories['genomic_unit'].create_genomic_unit(new_genomic_unit)

    if omic_unit['type'] is OmicUnitType.HGVS_VARIANT:
        transcript = omic_unit['unit'].split(':')[0]
        transcript_without_version = re.sub(r'\..*', '', transcript)
        omic_unit['genomic_build'] = 'hg19'
        omic_unit['transcript'] = transcript_without_version

    annotation_service = AnnotationService(repositories['annotation_config'])
    annotation_service.queue_annotation_tasks([omic_unit], annotation_task_queue)

    return annotation_service.process_tasks(
        annotation_queue=annotation_task_queue,
        genomic_unit_collection=repositories['genomic_unit'],
        annotation_manifest_collection=repositories['annotation_manifest'],
        omic_unit=omic_unit
    )
