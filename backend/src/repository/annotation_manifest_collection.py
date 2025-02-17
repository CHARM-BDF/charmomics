from pymongo import ReturnDocument

from src.core.annotation_unit import AnnotationUnit

# create logger
import logging

logger = logging.getLogger(__name__)


class AnnotationManifestCollection:
    """ Repository to keep track of which annotation versions are used in CHARMomics """

    def __init__(self, annotation_manifest_collection):
        """ Initalizes with the 'PyMongo' Collection object for the annotation manifest collection """

        self.collection = annotation_manifest_collection

    def all(self):
        """ Returns all annotations available in CHARMomics with their versions """

        return list(self.collection.find())

    def get_manifest_dataset_config(self, genomic_unit: str, dataset_name: str):
        """ Returns an individual dataset manifest """

        dataset_attribute = f"manifest.{dataset_name}"

        projection = {"manifest.$": 1}
        query = {"genomic_unit": genomic_unit, dataset_attribute: {'$exists': True}}
        genomic_unit_manifest = self.collection.find_one(query, projection)

        if not genomic_unit_manifest:
            return None

        manifest_entry = next((dataset for dataset in genomic_unit_manifest['manifest'] if dataset_name in dataset),
                              None)

        return {
            "data_set": dataset_name, "data_source": manifest_entry[dataset_name]['data_source'],
            "version": manifest_entry[dataset_name]['version']
        }

    def add_dataset_to_manifest(self, annotation_unit: AnnotationUnit):
        """ Adds this dataset and its version to the CHARMomics manifest. """

        dataset = {
            annotation_unit.get_dataset_name(): {
                'data_source': annotation_unit.get_dataset_source(), 'version': annotation_unit.get_version()
            }
        }

        updated_document = self.collection.find_one_and_update({"genomic_unit": annotation_unit.genomic_unit['unit']},
                                                               {"$push": {"manifest": dataset}},
                                                               upsert=True,
                                                               return_document=ReturnDocument.AFTER)

        return updated_document
