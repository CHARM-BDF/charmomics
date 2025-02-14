"""Tests for annotation manifest collection"""

import pytest

from src.core.annotation_unit import AnnotationUnit


def test_get_all_annotation_manifest(annotation_manifest_collection):
    """ Gets all entries in the annotation manifest collection """

    assert len(annotation_manifest_collection.all()) == 1


def test_get_manifest_dataset_config(annotation_manifest_collection):
    """ Gets the annotation manifest for gene VMA21 and OMIM dataset """

    # There's only one entry in the manifest for fixtures, get the first one which is VMA21
    annotation_manifest_collection.collection.find_one.return_value = annotation_manifest_collection.all()[0]

    expected = {"data_set": "OMIM", "data_source": "Ensembl", "version": "2024-09-06"}

    actual = annotation_manifest_collection.get_manifest_dataset_config("VMA21", "OMIM")

    assert expected == actual


def test_add_dataset_to_manifest(annotation_manifest_collection, annotation_unit_vma21_worm_url):
    """ Tests adding a new dataset and genomic unit to the annotation manifest """

    annotation_manifest_collection.add_dataset_to_manifest(annotation_unit_vma21_worm_url)

    annotation_manifest_collection.collection.find_one_and_update.assert_called_with({'genomic_unit': 'VMA21'}, {
        '$push':
            {'manifest': {'C-Elegens_Worm_Base_url': {'data_source': 'Ensembl', 'version': 'latest-test-version'}}}
    },
                                                                                     upsert=True,
                                                                                     return_document=True)


## Fixtures ##


@pytest.fixture(name="annotation_unit_vma21_worm_url")
def fixture_annotation_unit_vma21():
    """ Returns the annotation unit for the genomic unit VMA21 and the dataset C-Elegens_Worm_Base_url """

    genomic_unit = {'unit': 'VMA21'}

    dataset = {
        "data_set": "C-Elegens_Worm_Base_url", "data_source": "Ensembl", "genomic_unit_type": "gene",
        "annotation_source_type": "http",
        "base_string": "https://www.alliancegenome.org/api/gene/{C-Elegens Gene Identifier}",
        "attribute": "{ \"ClinGen_gene_url\": .ClinGen_gene_url }", "dependencies": ["C-Elegens Gene Identifier"],
        "delay_count": 5, "versioning_type": "rest", "version_url": "https://www.alliancegenome.org/api/releaseInfo",
        "version_attribute": ".releaseVersion"
    }

    annotation_unit = AnnotationUnit(genomic_unit, dataset)
    annotation_unit.set_latest_version("latest-test-version")

    return annotation_unit
