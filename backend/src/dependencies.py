""" Franklin dependencies that are shared within the entire application """

from pymongo import MongoClient

from .config import get_settings
from .database import Database

settings = get_settings()

mongodb_connection_uri = f"mongodb://{settings.mongodb_host}/{settings.mongodb_db}"
mongodb_client = MongoClient(mongodb_connection_uri)

# Database/Repositories
database = Database(mongodb_client)
