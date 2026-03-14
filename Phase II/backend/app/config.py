"""
Application configuration using pydantic-settings
Loads environment variables from .env file
SQLite se PostgreSQL (Neon) par shift kiya gaya hai
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "JWT Authentication and Tasks API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    APP_ENV: str = "development"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000
    
    # Database (Neon PostgreSQL)
    # SQLite se PostgreSQL par shift: DATABASE_URL format
    # postgresql://user:password@host/neondb?sslmode=require
    DATABASE_URL: str
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # API Prefix (for route fix)
    API_PREFIX: str = "/api"

    # CORS (Next.js frontend ke liye)
    # http://localhost:3000 allow kiya gaya hai
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:8000"
    
    # Better Auth (Next.js ke liye)
    BETTER_AUTH_SECRET: str = ""
    BETTER_AUTH_URL: str = "http://localhost:3000"
    
    # Frontend URLs
    NEXT_PUBLIC_APP_URL: str = "http://localhost:3000"
    NEXT_PUBLIC_API_URL: str = "http://localhost:8000"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """
        Parse comma-separated origins into list
        CORS middleware ke liye
        """
        if not self.ALLOWED_ORIGINS:
            return ["http://localhost:3000"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
