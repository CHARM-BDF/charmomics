"""Supports the queueing and processing of genomic unit annotation"""
import concurrent
import logging

from .annotation_helper import annotation_log_label
from .annotation_process import AnnotationProcess
from .annotation_queue import AnnotationQueue
from .annotation_unit import AnnotationUnit

from src.repository.annotation_config_collection import AnnotationConfigCollection
from src.repository.annotation_manifest_collection import AnnotationManifestCollection
from src.repository.genomic_unit_collection import GenomicUnitCollection

# create logger
logger = logging.getLogger(__name__)


class AnnotationService:
    """
    Creates and manages annotating genomic units for cases.
    """

    def __init__(self, annotation_config_collection: AnnotationConfigCollection):
        """Initializes the annotation service and injects the collection that has the annotation configuration"""
        self.annotation_config_collection = annotation_config_collection

    def queue_annotation_tasks(self, units_to_annotate, annotation_task_queue: AnnotationQueue):
        """ Uses the list of genomic units and the list of types to queue annotation operations. """

        annotation_configuration = self.annotation_config_collection.datasets_to_annotate_for_units(units_to_annotate)

        for genomic_unit in units_to_annotate:
            genomic_unit_type = genomic_unit["type"].value
            for dataset in annotation_configuration[genomic_unit_type]:
                annotation_unit_queued = AnnotationUnit(genomic_unit, dataset)
                annotation_task_queue.put(annotation_unit_queued)

    @staticmethod
    def process_tasks(
        annotation_queue: AnnotationQueue, genomic_unit_collection: GenomicUnitCollection,
        annotation_manifest_collection: AnnotationManifestCollection
    ):  # pylint: disable=too-many-branches,too-many-locals
        """Processes items that have been added to the queue"""
        logger.info("%s Processing annotation tasks queue ...", annotation_log_label())

        processor = AnnotationProcess(annotation_queue, genomic_unit_collection, annotation_manifest_collection)

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as task_executor:
            processor.set_task_executor(task_executor)

            while not processor.annotation_unit_queue_empty() or processor.are_tasks_processing():
                annotation_unit = processor.queue.get()

                processor.process_annotation_unit(annotation_unit)

                for task_future in concurrent.futures.as_completed(processor.annotation_task_futures):
                    processor.on_task_complete(task_future)

            logger.info("%s Processing annotation tasks queue complete", annotation_log_label())

        processor.log_dataset_failures()
        logger.info("%s Annotation BackgroundTask thread ending", annotation_log_label())
