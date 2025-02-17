""" CHARMomics dependencies that are shared within the entire application """

from pymongo import MongoClient

from src.config import get_settings
from src.core.annotation import AnnotationQueue
from src.database import Database

settings = get_settings()

# Database Setup
mongodb_connection_uri = f"mongodb://{settings.mongodb_host}/{settings.mongodb_db}"
mongodb_client = MongoClient(mongodb_connection_uri)
database = Database(mongodb_client)

# Annotation Setup
annotation_queue = AnnotationQueue()
