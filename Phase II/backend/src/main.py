"""
FastAPI application entry point
User Authentication API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.src.core.config import settings
from backend.src.core.database import create_db_and_tables
from backend.src.core.cors import setup_cors
from backend.src.api.routes import auth

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    
    Returns:
        Configured FastAPI application instance
    """
    # Create FastAPI application
    app = FastAPI(
        title=settings.APP_NAME,
        description="RESTful API for user authentication with JWT tokens",
        version=settings.APP_VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Setup CORS middleware
    setup_cors(app, settings.allowed_origins_list)
    
    # Register event handlers
    @app.on_event("startup")
    def on_startup() -> None:
        """Initialize database tables on application startup"""
        logger.info("Starting up application...")
        create_db_and_tables()
        logger.info("Database tables created successfully")
    
    # Include API routers
    app.include_router(auth.router)
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "version": settings.APP_VERSION}
    
    logger.info("Application created successfully")
    
    return app


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "backend.src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
