import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    api_title: str = "Query Router API"
    api_description: str = "A backend API that routes natural language queries to appropriate tools"
    api_version: str = "1.0.0"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # OpenAI Configuration
    gemini_api_key: str | None = None
    gemini_model_name: str = "gemini-2.0-flash"
    
    # OpenWeatherMap Configuration
    openweather_api_key: str | None = None
    
    # Tool Configuration
    default_location: str = "London"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings() 