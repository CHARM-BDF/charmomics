""" Annotation endpoint routes that handle all things annotation within the application """

import logging
import re

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException

from src.core.annotation import AnnotationService
from src.dependencies import database, annotation_queue
from src.enums import GenomicUnitType

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/annotation", tags=["annotation"], dependencies=[Depends(database)])


@router.post("/gene/{gene}")
def annotation_gene_genomic_unit(
    gene: str,
    background_tasks: BackgroundTasks,
    repositories=Depends(database),
    annotation_task_queue=Depends(annotation_queue)
):
    """ Annotation endpoint to annotate a gene genomic unit """
    units_to_annotate = [{"unit": gene, "type": GenomicUnitType.GENE}]

    genomic_unit = {
        'type': GenomicUnitType.GENE,
        'unit': gene,
    }

    genomic_unit_exist = repositories["genomic_unit"].find_genomic_unit(genomic_unit)

    if not genomic_unit_exist:
        genomic_gene_data = {"gene_symbol": gene, "gene": gene, "annotations": []}
        repositories['genomic_unit'].create_genomic_unit(genomic_gene_data)

    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks(units_to_annotate, annotation_task_queue)

    background_tasks.add_task(
        AnnotationService.process_tasks, annotation_task_queue, repositories['annotation_manifest'],
        repositories['genomic_unit']
    )

    return {"name": f"{gene} annotations queued."}


@router.post("/variant/{hgvs_variant}")
def annotation_variant_transcript_genomic_unit(
    hgvs_variant: str,
    background_tasks: BackgroundTasks,
    repositories=Depends(database),
    annotation_task_queue=Depends(annotation_queue)
):

    genomic_unit = {
        'type': GenomicUnitType.HGVS_VARIANT,
        'unit': hgvs_variant,
    }

    genomic_unit_exist = repositories["genomic_unit"].find_genomic_unit(genomic_unit)

    if not genomic_unit_exist:
        genomic_gene_data = {"hgvs_variant": hgvs_variant, "transcripts": [], "annotations": []}
        repositories['genomic_unit'].create_genomic_unit(genomic_gene_data)

    transcript = hgvs_variant.split(':')[0]
    transcript_without_version = re.sub(r'\..*', '', transcript)

    units_to_annotate = [{
        "unit": hgvs_variant,
        "type": GenomicUnitType.HGVS_VARIANT,
        "genomic_build": 'hg19',
        "transcript": transcript_without_version,
    }]

    annotation_service = AnnotationService(repositories["annotation_config"])
    annotation_service.queue_annotation_tasks(units_to_annotate, annotation_task_queue)
    background_tasks.add_task(
        AnnotationService.process_tasks, annotation_task_queue, repositories['annotation_manifest'],
        repositories['genomic_unit']
    )

    return {"name": f"{hgvs_variant} annotations queued."}


@router.get("/gene/{gene}")
def fetch_gene_annotations(
    gene: str,
    repositories=Depends(database),
):
    """ Annotation endpoint to fetch annotations for a gene genomic unit """

    genomic_unit = {
        'type': GenomicUnitType.GENE,
        'unit': gene,
    }

    genomic_unit_document = repositories["genomic_unit"].find_genomic_unit(genomic_unit)

    if genomic_unit_document is None:
        raise HTTPException(status_code=404, detail=f"No annotations for '{gene}' found. Please queue annotations!")

    if "_id" in genomic_unit_document:
        genomic_unit_document.pop("_id", None)

    return genomic_unit_document


@router.get("/variant/{hgvs_variant}")
def fetch_variant_transcript_annotations(
    hgvs_variant: str,
    repositories=Depends(database),
):
    """ Annotation endpoint to fetch annotations for a gene genomic unit """

    genomic_unit = {
        'type': GenomicUnitType.HGVS_VARIANT,
        'unit': hgvs_variant,
    }

    genomic_unit_document = repositories["genomic_unit"].find_genomic_unit(genomic_unit)

    if genomic_unit_document is None:
        raise HTTPException(
            status_code=404, detail=f"No annotations for '{hgvs_variant}' found. Please queue annotations!"
        )

    if "_id" in genomic_unit_document:
        genomic_unit_document.pop("_id", None)

    return genomic_unit_document
