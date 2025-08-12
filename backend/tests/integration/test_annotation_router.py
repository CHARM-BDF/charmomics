"""Routes dedicated for annotation within the system"""

from unittest.mock import patch

from fastapi import BackgroundTasks

from src.core.annotation import AnnotationService


def test_get_annotations_by_gene(client, mock_repositories, gene_vma21_annotations_json):
    """ Tests the endpoint that queues a requested gene annotation """

    mock_repositories['genomic_unit'].collection.find_one.return_value = gene_vma21_annotations_json

    response = client.get("/annotation/gene/VMA21")

    assert response.status_code == 200

    actual = response.json()

    assert len(actual) == 3
    assert actual['gene_symbol'] == "VMA21"
    assert len(actual['annotations']) == 6


def test_queue_annotations_by_gene(
    client, mock_repositories, mock_annotation_queue, gene_vma21_annotations_json, annotations_config_collection_json,
    annotations_manifest_collection_json
):
    """ Tests the endpoint that fetches a stored gene's annotations from mongo """

    mock_repositories['annotation_config'].collection.find.return_value = annotations_config_collection_json
    mock_repositories['annotation_manifest'].collection.find.return_value = annotations_manifest_collection_json
    mock_repositories['genomic_unit'].collection.find_one.return_value = gene_vma21_annotations_json

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:

        response = client.post("/annotation/gene/VMA21")

        assert mock_annotation_queue.put.call_count == 7

        mock_background_add_task.assert_called_once_with(
            AnnotationService.process_tasks, mock_annotation_queue, mock_repositories['annotation_manifest'],
            mock_repositories['genomic_unit']
        )

    assert response.status_code == 200

    assert response.json()['name'] == "VMA21 annotations queued."


def test_queue_annotations_by_variant(
    client, mock_repositories, mock_annotation_queue, variant_nm001017980_3_c_164g_t_annotations_json,
    annotations_config_collection_json, annotations_manifest_collection_json
):
    """ Tests the endpoint that fetches a stored hgvs variant's annotations from mongo """
    mock_repositories['annotation_config'].collection.find.return_value = annotations_config_collection_json
    mock_repositories['annotation_manifest'].collection.find.return_value = annotations_manifest_collection_json
    mock_repositories['genomic_unit'].collection.find_one.return_value = variant_nm001017980_3_c_164g_t_annotations_json

    with patch.object(BackgroundTasks, "add_task", return_value=None) as mock_background_add_task:

        response = client.post("/annotation/variant/NM001017980_3_c_164G_T")

        assert mock_annotation_queue.put.call_count == 4

        mock_background_add_task.assert_called_once_with(
            AnnotationService.process_tasks, mock_annotation_queue, mock_repositories['annotation_manifest'],
            mock_repositories['genomic_unit']
        )

    assert response.status_code == 200

    assert response.json()['name'] == "NM001017980_3_c_164G_T annotations queued."


def test_get_annotations_by_variant(client, mock_repositories, variant_nm001017980_3_c_164g_t_annotations_json):
    """ Tests the endpoint that queues a requested hgvs variant annotation """
    mock_repositories['genomic_unit'].collection.find_one.return_value = variant_nm001017980_3_c_164g_t_annotations_json

    response = client.get("/annotation/variant/NM001017980_3_c_164G_T")

    assert response.status_code == 200

    actual = response.json()

    assert len(actual) == 3
    assert actual['hgvs_variant'] == "NM_001017980.3:c.164G>T"
    assert len(actual['annotations']) == 2
