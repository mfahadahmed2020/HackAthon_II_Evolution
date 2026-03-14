"""
Backend entry point for Docker and production deployment
Re-exports app from app.main for uvicorn compatibility
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
