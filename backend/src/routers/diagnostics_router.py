""" Annotation endpoint routes that handle all things annotation within the application """
import logging
import re

from fastapi import APIRouter, Depends, HTTPException

from src.core.annotation import AnnotationService
from src.dependencies import database, annotation_queue
from src.enums import ReportUnitType, DiagnosticTestType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/diagnostic", tags=["diagnostic tests"], dependencies=[Depends(database)])


@router.post("/")
def get_diagnostic_test(
    diagnostic_test: DiagnosticTestType,
    repositories=Depends(database),
    annotation_task_queue=Depends(annotation_queue)
):
    """ Initiates annotation for diagnostic tests and returns all diagnostic tests """

    ## Create entries for the diagnostic tests if they don't exist

    omic_unit = {'unit': diagnostic_test.value, 'type': ReportUnitType.DIAGNOSTIC_TEST}

    logger.info(omic_unit)

    test_exist = repositories['genomic_unit'].find_genomic_unit(omic_unit)

    logger.info(test_exist)

    if not test_exist:
        new_genomic_unit = {"diagnostic_test": omic_unit['unit'], 'annotations': []}
        repositories['genomic_unit'].create_genomic_unit(new_genomic_unit)

    annotation_service = AnnotationService(repositories['annotation_config'])
    annotation_service.queue_annotation_task(omic_unit, annotation_task_queue)

    return annotation_service.process_tasks(
        annotation_queue=annotation_task_queue,
        genomic_unit_collection=repositories['genomic_unit'],
        annotation_manifest_collection=repositories['annotation_manifest'],
        omic_unit=omic_unit
    )
