"""
FastAPI application entry point
JWT Authentication and Tasks API
Route Fix Complete: Using app/routers/ with /api prefix
Phase 5: WebSocket support for real-time updates
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import create_db_and_tables
from app.routers import auth, todos, categories, analytics
from app.websocket import manager, authenticate_websocket


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="RESTful API for user authentication, task management, categories, and real-time updates with JWT tokens",
    version=settings.APP_VERSION,
)


# CORS middleware - configurable origins from environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    """
    Initialize database tables on application startup
    """
    create_db_and_tables()


# Include API routers with /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(todos.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")


# ============ WebSocket Endpoint ============
# Phase 5: Real-time Updates

@app.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates
    
    Roman Urdu: Real-time updates ke liye WebSocket connection
    
    Query Parameters:
        token: JWT access token for authentication
    
    Message Types:
        - connected: Connection established
        - task.created: New task created
        - task.updated: Task updated
        - task.deleted: Task deleted
        - analytics.updated: Analytics data changed
    
    Usage (Frontend):
        const ws = new WebSocket(`ws://localhost:8000/api/ws?token=${accessToken}`);
        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'task.updated') {
                // Update UI
            }
        };
    """
    # Authenticate WebSocket connection
    # Roman Urdu: WebSocket connection ko authenticate karna
    try:
        user_id = await authenticate_websocket(websocket)
    except WebSocketDisconnect:
        return  # Connection already closed by authenticate_websocket
    
    # Connect to manager
    # Roman Urdu: Connection manager se connect karna
    await manager.connect(websocket, user_id)
    
    try:
        # Keep connection alive and handle incoming messages
        # Roman Urdu: Connection ko alive rakhna aur incoming messages handle karna
        while True:
            # Wait for messages from client
            # Roman Urdu: Client se messages ka wait karna
            try:
                data = await websocket.receive_text()
                message = data  # Simple echo or process message
                
                # Echo message back (for testing)
                # Roman Urdu: Testing ke liye message echo karna
                await websocket.send_json({
                    "type": "echo",
                    "data": message,
                    "timestamp": "Message received"
                })
            
            except WebSocketDisconnect:
                # Client disconnected
                # Roman Urdu: Client disconnect ho gaya
                break
    
    except Exception as e:
        # Handle unexpected errors
        # Roman Urdu: Unexpected errors handle karna
        print(f"WebSocket error: {e}")
    
    finally:
        # Disconnect from manager
        # Roman Urdu: Connection manager se disconnect karna
        await manager.disconnect(websocket, user_id)


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns API status and version
    """
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "JWT Authentication and Tasks API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "endpoints": {
            "auth": "/api/register, /api/login",
            "todos": "/api/todos (GET, POST), /api/todos/{id} (GET, PUT, DELETE)"
        }
    }
