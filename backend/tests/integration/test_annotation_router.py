""" Routes dedicated for annotation within the system """


def test_annotate_gene_omic_unit(
    client, mock_repositories, mock_annotation_queue, gene_vma21_annotations_json, annotations_config_collection_json,
    annotations_manifest_collection_json
):
    """
    Tests the endpoint that queues gene annotation tasks and recieves a response with a gene unit from the genomic unit 
    collection
    """
    expected = {"status": 200, "queue_call_count": 8, "annotation_count": 6}

    mock_repositories['annotation_config'].collection.find.return_value = annotations_config_collection_json
    mock_repositories['annotation_manifest'].collection.find.return_value = annotations_manifest_collection_json
    mock_repositories['genomic_unit'].collection.find_one.return_value = gene_vma21_annotations_json

    response = client.post("/annotation/?type=gene&name=VMA21")

    actual = response.json()

    assert mock_annotation_queue.put.call_count == expected['queue_call_count']
    assert response.status_code == expected['status']
    assert len(actual['annotations']) == expected['annotation_count']


def test_annotate_hgvs_variant_omic_unit(
    client, mock_repositories, mock_annotation_queue, variant_nm001017980_3_c_164g_t_annotations_json,
    annotations_config_collection_json, annotations_manifest_collection_json
):
    """
    Tests the endpoint that queues hgvs_variant annotations and recieves a response with a hgvs_variant unit from the
    genomic unit collection
    """

    expected = {"status": 200, "queue_call_count": 4, "annotation_count": 2, "transcript_count": 2}

    mock_repositories['annotation_config'].collection.find.return_value = annotations_config_collection_json
    mock_repositories['annotation_manifest'].collection.find.return_value = annotations_manifest_collection_json
    mock_repositories['genomic_unit'].collection.find_one.return_value = variant_nm001017980_3_c_164g_t_annotations_json

    response = client.post("/annotation/?type=hgvs_variant&name=NM_001017980.3:c.164G>T")

    actual = response.json()

    assert mock_annotation_queue.put.call_count == expected['queue_call_count']
    assert response.status_code == expected['status']
    assert len(actual['annotations']) == expected['annotation_count']
    assert len(actual['transcripts']) == expected['transcript_count']
