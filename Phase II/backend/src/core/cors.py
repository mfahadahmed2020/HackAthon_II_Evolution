"""
CORS middleware configuration
Allows cross-origin requests from configured frontend URLs
"""

from fastapi.middleware.cors import CORSMiddleware
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI


def setup_cors(app: "FastAPI", allowed_origins: list[str]) -> None:
    """
    Configure CORS middleware for the FastAPI application
    
    Args:
        app: FastAPI application instance
        allowed_origins: List of allowed origin URLs
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Authorization", "Content-Type", "Accept"],
        max_age=600,  # Cache preflight requests for 10 minutes
    )


def get_cors_config() -> dict:
    """
    Get CORS configuration dictionary
    Can be used for custom middleware setup
    """
    return {
        "allow_origins": ["http://localhost:3000"],
        "allow_credentials": True,
        "allow_methods": ["*"],
        "allow_headers": ["*"],
    }
