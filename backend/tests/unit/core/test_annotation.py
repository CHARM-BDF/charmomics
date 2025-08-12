""" Tests to verify annotation tasks """

from unittest.mock import Mock, patch

import pytest

from src.core.annotation import AnnotationService
from src.repository.annotation_manifest_collection import AnnotationManifestCollection
from src.repository.genomic_unit_collection import GenomicUnitCollection


def test_queuing_annotations_for_genomic_units(genomic_units_to_annotate, annotation_config_collection):
    """Verifies annotations are queued according to the specific genomic units"""
    annotation_service = AnnotationService(annotation_config_collection)
    mock_queue = Mock()
    annotation_service.queue_annotation_tasks(genomic_units_to_annotate, mock_queue)
    assert mock_queue.put.call_count == 29

    actual_queued_genomic_units = [put_call.args[0].genomic_unit['unit'] for put_call in mock_queue.put.call_args_list]

    assert "NM_170707.3:c.745C>T" in actual_queued_genomic_units


def test_processing_annotation_tasks(process_annotation_tasks):
    """Verifies that each item on the annotation queue is read and executed"""
    assert process_annotation_tasks['http'].call_count == 18
    assert process_annotation_tasks['none'].call_count == 0
    assert process_annotation_tasks['forge'].call_count == 6
    assert process_annotation_tasks['subprocess'].call_count == 2

    assert process_annotation_tasks['extract'].call_count == 29

    assert process_annotation_tasks['version'].call_count == 4

    assert process_annotation_tasks['genomic_unit_collection'].find_genomic_unit_annotation_value.call_count == 23
    process_annotation_tasks['genomic_unit_collection'].annotate_genomic_unit.assert_called()


# Disabling PyLint due to this being a simple Mock adapter as a simple test harness for emulating mising a dependency
class SkipDepedencies:  # pylint: disable=too-few-public-methods
    """ A skip annotation dependencies helper class that allows tester to dictate which datasets to skip once to
    emulate a depedency not existing the first time when preparing an Annotation Task for annotation."""

    def __init__(self, dependencies_to_skip=None):
        """ Dictating the list of  of dataset names to emulate that dataset annotation not existing."""
        self.skip_tracker = {}
        self.to_skip = dependencies_to_skip if dependencies_to_skip else ["HGNC_ID"]

    def skip_hgncid_get_value_first_time_mock(self, *args):
        """ Mock method that tracks if the provided dependencies are one of the ones indicated to skip"""
        annotation_unit = args[0]
        name = annotation_unit.get_dataset_name()
        genomic_unit = annotation_unit.get_genomic_unit()
        should_skip = (name in self.to_skip and name not in self.skip_tracker)
        return self.skip_tracker.setdefault(name, None) if should_skip else f"{genomic_unit}-{name}-value"


@pytest.fixture(name="process_annotation_tasks")
def fixture_extract_and_annotate(annotation_queue, get_dataset_manifest_config):
    """
    Emulates processing the annotations for the VMA21's configured gene datasets
    """
    mock_extract_result = [{
        'data_set': 'mock_datset',
        'data_source': 'mock_source',
        'version': '0.0',
        'value': '9000',
    }]

    with (
        patch("src.core.annotation_task.AnnotationTaskInterface.extract",
              return_value=mock_extract_result) as extract_task_annotate,
        patch("src.core.annotation_task.AnnotationTaskInterface.extract_version", return_value='fake-version') as
        extract_task_version_annotate, patch("src.core.annotation_task.VersionAnnotationTask.annotate") as
        version_task_annotate, patch("src.core.annotation_task.ForgeAnnotationTask.annotate") as forge_task_annotate,
        patch("src.core.annotation_task.HttpAnnotationTask.annotate") as http_task_annotate,
        patch("src.core.annotation_task.NoneAnnotationTask.annotate") as none_task_annotate,
        patch("src.core.annotation_task.SubprocessAnnotationTask.annotate") as subprocess_task_annotate
    ):
        skip_depends = SkipDepedencies()
        mock_genomic_unit_collection = Mock(spec=GenomicUnitCollection)
        mock_annotation_manifest_collection = Mock(spec=AnnotationManifestCollection)
        mock_genomic_unit_collection.find_genomic_unit_annotation_value.side_effect = (
            skip_depends.skip_hgncid_get_value_first_time_mock
        )
        dependency_dataset = get_dataset_manifest_config("VMA21", 'HGNC_ID')
        mock_annotation_manifest_collection.get_manifest_dataset_config.return_value = dependency_dataset
        mock_genomic_unit_collection.annotation_exist.return_value = False

        AnnotationService.process_tasks(
            annotation_queue, mock_annotation_manifest_collection, mock_genomic_unit_collection
        )
        yield {
            'extract': extract_task_annotate, 'version': version_task_annotate, 'http': http_task_annotate,
            'none': none_task_annotate, 'forge': forge_task_annotate, 'subprocess': subprocess_task_annotate,
            'genomic_unit_collection': mock_genomic_unit_collection, 'extract_version': extract_task_version_annotate
        }
