""" Module manages interface to the repository in the data layer that stores the persistent state of the application """

# pylint: disable=too-few-public-methods

from src.repository.annotation_config_collection import AnnotationConfigCollection
from src.repository.annotation_manifest_collection import AnnotationManifestCollection
from src.repository.genomic_unit_collection import GenomicUnitCollection


class Database:
    """
    Interface for collections and additional resources for the persistent state of the application.
    
    Utilize the 'connect(client)' method to accept a configured MongoDB database client. MongoDB does not connect
    until the first query on a MongoDB collection is executed.
    """

    def __init__(self, client):
        self.database_client = client

        # "An important note about collections (and databases) in MongoDB is that they are created lazily -
        # none of the above commands have actually performed any operations on the MongoDB server. Collections and
        # databases are created when the first document is inserted into them. This is why it is safe to include these
        # operations within a constructor since there is not chance for failure creating allocating the object."
        #
        # https://pymongo.readthedocs.io/en/stable/tutorial.html#getting-a-collection
        self.database = self.database_client.charmomics_db
        self.collections = {
            "annotation_config": AnnotationConfigCollection(self.database['annotation_config']),
            "annotation_manifest": AnnotationManifestCollection(self.database['annotation_manifest']),
            "genomic_unit": GenomicUnitCollection(self.database['genomic_units'])
        }

    def __call__(self):
        """
        Returns the injected dependency instance to use for sharing the repository collections to routes
        See FastAPI docs to learn more https://fastapi.tiangolo.com/advanced/advanced-dependencies/#a-callable-instance
        """
        return self.collections
