from pymongo import ReturnDocument

from src.core.annotation_unit import AnnotationUnit


class AnnotationManifestCollection:
    """ Repository to keep track of which annotation versions are used in Franklin """

    def __init__(self, annotation_manifest_collection):
        """ Initalizes with the 'PyMongo' Collection object for the annotation manifest collection """

        self.collection = annotation_manifest_collection

    def all(self):
        """ Returns all annotations available in Franklin with their versions """

        return list(self.collection.find())

    def get_manifest_dataset_config(self, dataset_name: str):
        """ Returns an individual dataset manifest """

        manifest_entry = self.collection.find_one({dataset_name: {'$exists': True}})

        if not manifest_entry:
            return None

        return {
            "data_set": dataset_name, "data_source": manifest_entry[dataset_name]['data_source'],
            "version": manifest_entry[dataset_name]['version']
        }

    def add_dataset_to_manifest(self, annotation_unit: AnnotationUnit):
        """ Adds this dataset and its version to the Franklin manifest. """

        dataset = {
            annotation_unit.get_dataset_name(): {
                'data_source': annotation_unit.get_dataset_source(), 'version': annotation_unit.get_version()
            }
        }

        return self.collection.insert_one(dataset)
