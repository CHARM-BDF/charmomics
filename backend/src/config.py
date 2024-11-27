"""
Contains all the configuration variables used thoughout the application.
These parameters have the intention that they can be changed/modified at runtime to provide deployment configuration.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Settings for Franklin.  See https://fastapi.tiangolo.com/advanced/settings/
    for more details.
    """

    mongodb_host: str = "franklin-db"
    mongodb_db: str = "franklin_db"


@lru_cache()
def get_settings():
    """
    Returns the instance of initializing the settings.  Utilizing lru_cache caches the result so that it is only
    reading from the environment variables once for the settings, instead of multiple times.
    """
    return Settings()
