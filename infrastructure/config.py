from functools import lru_cache
from pydantic_settings import BaseSettings
import os

@lru_cache
def get_env_filename():
    runtime_env = os.getenv('ENV')
    return '.env' if runtime_env else '.env'

class EnvironmentSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DATABASE_URL: str

    REDIS_URL: str
    REDIS_HOST: str
    REDIS_BASE: int
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    
    API_BASE_URL: str

    class config:
        env_file = get_env_filename()
        env_file_enconding = 'utf-8'

@lru_cache
def get_environment_variable():
    return EnvironmentSettings()