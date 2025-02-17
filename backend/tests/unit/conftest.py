""" Fixture configuration used for all unit tests """

from unittest.mock import Mock

import queue
import pytest

from src.core.annotation import AnnotationService
from src.core.annotation_unit import AnnotationUnit
from src.enums import GenomicUnitType
from src.repository.annotation_config_collection import AnnotationConfigCollection
from src.repository.genomic_unit_collection import GenomicUnitCollection
from src.repository.annotation_manifest_collection import AnnotationManifestCollection

from ..test_utils import read_test_fixture, mock_mongo_collection


@pytest.fixture(name="annotation_config_collection_json")
def fixture_annotation_config_collection_json():
    """ Returns the json for the annotation configuration """

    return read_test_fixture("annotation-config.json")


@pytest.fixture(name="annotation_manifest_collection_json")
def fixture_annotation_manifest_collection_json():
    """ Returns the json for the annotation manifest """

    return read_test_fixture("annotation-manifest.json")


@pytest.fixture(name="gene_vma21_annotations_json")
def fixture_gene_annotation_json():
    """JSON for the annotations of the Gene VMA21"""
    return read_test_fixture("annotations-VMA21.json")


@pytest.fixture(name="variant_nm001017980_3_c_164g_t_annotations_json")
def fixture_hgvs_variant_json():
    """JSON for the annotations of the Gene VMA21"""
    return read_test_fixture("annotations-NM001017980_3_c_164G_T.json")


@pytest.fixture(name="genomic_unit_collection_json")
def fixture_genomic_unit_collection_json(gene_vma21_annotations_json, variant_nm001017980_3_c_164g_t_annotations_json):
    """Returns array of JSON for the genomic units within the collection"""
    return [gene_vma21_annotations_json, variant_nm001017980_3_c_164g_t_annotations_json]


@pytest.fixture(name="annotation_config_collection")
def fixture_annotation_config_collection(annotation_config_collection_json):
    """Returns the annotation collection for the datasets to be mocked"""
    mock_collection = mock_mongo_collection()
    mock_collection.find = Mock(return_value=annotation_config_collection_json)
    mock_collection.find_one = Mock(return_value=read_test_fixture("annotation-config.json"))
    return AnnotationConfigCollection(mock_collection)


@pytest.fixture(name="genomic_units_to_annotate")
def fixture_genomic_units_to_annotate():
    """ Mock units to annotate, can handle a list of units """

    return [{'unit': "LMNA", 'type': GenomicUnitType.GENE}, {'unit': "VMA21", 'type': GenomicUnitType.GENE},
            {'unit': "NM_001017980.3:c.164G>T", 'type': GenomicUnitType.HGVS_VARIANT},
            {'unit': "NM_170707.3:c.745C>T", 'type': GenomicUnitType.HGVS_VARIANT}]


# TODO: Carry over from Rosalution tests, no analysis in charmomics, at least yet
@pytest.fixture(name="genomic_units_with_types")
def fixture_genomic_units_with_types(genomic_units_to_annotate):
    """Returns the multiple analyses being mocked as an array """

    types = {unit['unit']: unit['type'] for unit in genomic_units_to_annotate}

    return types


@pytest.fixture(name='get_annotation_unit')
def get_standard_annotation_unit(annotation_config_collection_json, genomic_units_with_types):
    """
    Fixture factory method to create an AnnotationUnit from the available genomic units in the analyses from
    'analysis_collection_json' fixture. It searches the 'annotation_config_collection_json' to pair with
    the genomic unit to create an AnnotationUnit.

    {
      'VMA21': GenomicUnitType.GENE,
      'NM_001017980.3:c.164G>T': GenomicUnitType.HGVS_VARIANT
    }
    """

    def _create_annotation_unit(genomic_unit_name, dataset_name):
        """Method to create the Annotation Unit"""
        genomic_unit_type = genomic_units_with_types[genomic_unit_name]
        genomic_unit = {'unit': genomic_unit_name, 'type': genomic_unit_type}
        dataset_config = next((unit for unit in annotation_config_collection_json if unit['data_set'] == dataset_name),
                              None)

        return AnnotationUnit(genomic_unit, dataset_config)

    return _create_annotation_unit


@pytest.fixture(name="annotation_queue")
def fixture_cpam0046_annotation_queue(genomic_units_to_annotate, annotation_config_collection):
    """ Returns an thread-safe annotation queue with tasks """

    test_queue = queue.Queue()
    annotation_service = AnnotationService(annotation_config_collection)
    annotation_service.queue_annotation_tasks(genomic_units_to_annotate, test_queue)

    return test_queue


@pytest.fixture(name='get_dataset_manifest_config')
def get_dataset_manifest_config(annotation_manifest_collection_json):
    """Fixture factory method to create an dataset from the genomic unit information and name of the datset."""

    def _create_dataset_manifest(genomic_unit, dataset_name):
        """Method to create the dataset manifest config"""

        genomic_unit_manifest = next(
            (item for item in annotation_manifest_collection_json if item['genomic_unit'] == genomic_unit), None
        )

        dataset_manifest = next((item for item in genomic_unit_manifest['manifest'] if dataset_name in item), None)

        dataset_config = {
            "data_set": dataset_name, "data_source": dataset_manifest[dataset_name]['data_source'],
            "version": dataset_manifest[dataset_name]['version']
        }

        return dataset_config

    return _create_dataset_manifest


@pytest.fixture(name="genomic_unit_collection")
def fixture_genomic_unit_collection(genomic_unit_collection_json):
    """Returns a genomic unit collection"""

    mock_collection = mock_mongo_collection()
    mock_collection.find = Mock(return_value=genomic_unit_collection_json)

    return GenomicUnitCollection(mock_collection)


@pytest.fixture(name="annotation_manifest_collection")
def fixture_annotation_manifest_collection(annotation_manifest_collection_json):
    """ Returns an annotation manifest collection """

    mock_collection = mock_mongo_collection()
    mock_collection.find = Mock(return_value=annotation_manifest_collection_json)
    mock_collection.find_one = Mock()
    mock_collection.find_one_and_update = Mock()

    return AnnotationManifestCollection(mock_collection)


@pytest.fixture(name='get_annotation_json')
def get_annotation_json(genomic_unit_collection_json):
    """Fixture factory method to create an return the JSON from the genomic unit """

    def _get_annotation_json(genomic_unit_name, genomic_unit_type):
        """ Provides a genomic unit from the genomic unit collection, otherwise returns false"""

        unit_type = genomic_unit_type.value
        return next((
            unit for unit in genomic_unit_collection_json if unit_type in unit and unit[unit_type] == genomic_unit_name
        ), None)

    return _get_annotation_json
