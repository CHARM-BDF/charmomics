""" Tests routes dedicated for annotating and returning diagnostic tests within the system """


def test_annotate_diagnostic_test(
    client, mock_repositories, mock_annotation_queue, annotations_config_collection_json,
    annotations_manifest_collection_json, diagnostic_test_microsatellite_instability_json
):
    """ Tests the endpoint that queues a single annotation for a diagnostic test """

    mock_repositories['annotation_config'].collection.find.return_value = annotations_config_collection_json
    mock_repositories['annotation_manifest'].collection.find.return_value = annotations_manifest_collection_json
    mock_repositories['genomic_unit'].collection.find_one.return_value = diagnostic_test_microsatellite_instability_json

    response = client.post("/diagnostic/?diagnostic_test=microsatellite_instability")

    actual = response.json()

    assert mock_annotation_queue.put.call_count == 1
    assert response.status_code == 200
    assert len(actual['annotations']) == 1
