""" Test Fixtures for integration tests """

from unittest.mock import Mock

import pytest

from fastapi.testclient import TestClient

from src.config import get_settings, Settings
from src.database import Database
from src.dependencies import database, annotation_queue
from src.main import app

from ..test_utils import mock_mongo_collection, read_test_fixture


@pytest.fixture(name="client", scope="class")
def test_application_client():
    """A class scoped FastApi Test Client"""
    return TestClient(app)


@pytest.fixture(name="mock_annotation_queue", scope="class")
def mock_queue():
    """A mocked Python queue used to verify if annotation tasks are created"""
    annotation_queue.annotation_queue = Mock()
    return annotation_queue.annotation_queue


@pytest.fixture(name="mock_repositories", scope="class")
def mock_database_collections():
    """A mocked database client which overrides the database depedency injected"""
    mock_database_client = Mock()

    mock_database_client.charmomics_db = {
        "annotation_manifest": mock_mongo_collection(),
        "annotation_config": mock_mongo_collection(),
        "genomic_units": mock_mongo_collection(),
    }

    mock_database = Database(mock_database_client)
    app.dependency_overrides[database] = mock_database
    yield mock_database.collections
    app.dependency_overrides.clear()


@pytest.fixture(name="mock_settings")
def mock_application_settings(settings_json):
    """The mocked settings which overrides the applications need for environment variables or .env file"""
    fake_settings = Settings(**settings_json)

    def mock_get_settings():
        return fake_settings

    app.dependency_overrides[get_settings] = mock_get_settings
    yield fake_settings
    app.dependency_overrides.clear()


@pytest.fixture(name="annotations_manifest_collection_json")
def fixture_annotations_manifest_collection_json():
    """JSON for the entire annotations manifest collection"""
    return read_test_fixture("annotation-manifest.json")


@pytest.fixture(name="annotations_config_collection_json")
def fixture_annotations_config_collection_json():
    """JSON for the entire annotations configuration collection"""
    return read_test_fixture("annotation-config.json")


@pytest.fixture(name="genomic_units_collection_json")
def fixture_genomic_unit_collection_json(gene_vma21_annotations_json, variant_nm001017980_3_c_164g_t_annotations_json):
    """JSON for the genomic units collection"""
    return [gene_vma21_annotations_json, variant_nm001017980_3_c_164g_t_annotations_json]


@pytest.fixture(name="settings_json")
def fixture_settings_json():
    """Returns the settings for a charmomics. Mostly used for security functionality/testing"""
    return read_test_fixture("application_settings.json")


@pytest.fixture(name="gene_vma21_annotations_json")
def fixture_gene_annotations_json():
    """JSON for the annotations of the Gene VMA21"""
    return read_test_fixture("annotations-VMA21.json")


@pytest.fixture(name="variant_nm001017980_3_c_164g_t_annotations_json")
def fixture_hgvs_variant_json():
    """JSON for the annotations of the Gene VMA21"""
    return read_test_fixture("annotations-NM001017980_3_c_164G_T.json")
