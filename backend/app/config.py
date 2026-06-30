from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application Settings
    Loads configuration from the .env file automatically.
    """
    PROJECT_NAME: str = "Job Portal API"
    API_V1_STR: str = "/api/v1"
    
    DATABASE_URL: str
    
    # JWT Authentication configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings() -> Settings:
    """
    LRU cached function to return settings. 
    Ensures that the settings are loaded only once.
    """
    return Settings()
