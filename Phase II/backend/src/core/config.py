"""
Application configuration
Loads settings from environment variables
"""

from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Application
    APP_NAME: str = "User Authentication API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = ""
    
    # JWT Settings
    BETTER_AUTH_SECRET: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440  # 24 hours
    
    # CORS
    FRONTEND_URL: str = "http://localhost:3000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Get list of allowed origins for CORS"""
        origins = [self.FRONTEND_URL]
        
        # Add production URLs if needed
        # origins.extend(["https://your-production-domain.com"])
        
        return origins
    
    @property
    def access_token_expire_minutes(self) -> int:
        """Get JWT expiration time in minutes"""
        return self.JWT_EXPIRATION_MINUTES
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Validate required settings
if not settings.BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is required")

if len(settings.BETTER_AUTH_SECRET) < 32:
    raise ValueError("BETTER_AUTH_SECRET must be at least 32 characters long")

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")
