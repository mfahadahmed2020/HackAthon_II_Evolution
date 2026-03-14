"""
WebSocket Manager for Real-time Updates
Roman Urdu: WebSocket Manager - Real-time updates ke liye connection manage karta hai

Features:
- ConnectionManager: WebSocket connections ko track karta hai (user_id wise)
- Authentication: JWT token se user authenticate karta hai
- Broadcast: User ke saare connected tabs ko message bhejta hai
- Multi-tab Sync: localStorage events ke saath cross-tab synchronization

Roman Urdu Comments:
- Yeh module real-time updates enable karta hai bina page refresh ke
- Jab ek tab mein task update hota hai, saare tabs mein reflect hota hai
- WebSocket + localStorage combination use hota hai
"""

from fastapi import WebSocket, WebSocketDisconnect, HTTPException, status
from typing import Dict, List
from datetime import datetime
import json

from app.auth import verify_token
from app.schemas import TokenData


class ConnectionManager:
    """
    Manage WebSocket connections for real-time updates
    
    Roman Urdu: WebSocket connections ko manage karta hai - user_id ke hisaab se track karta hai
    
    Features:
    - Multiple connections per user (different tabs/devices)
    - User-based connection tracking
    - Broadcast to all user connections
    
    Usage:
        manager = ConnectionManager()
        
        # Connect
        await manager.connect(websocket, user_id)
        
        # Broadcast to user
        await manager.broadcast_to_user(user_id, {"type": "task.updated", "data": task})
        
        # Disconnect
        await manager.disconnect(websocket, user_id)
    """
    
    def __init__(self):
        """
        Initialize connection manager
        
        Roman Urdu: Connection manager initialize karta hai
        Structure: {user_id: [websocket1, websocket2, ...]}
        """
        # Active connections per user
        # Roman Urdu: Har user ki active connections ki list
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        """
        Accept WebSocket connection and track it
        
        Roman Urdu: WebSocket connection accept karta hai aur track karta hai
        
        Args:
            websocket: WebSocket connection object
            user_id: Authenticated user ka ID
        
        Sends:
            {"type": "connected", "user_id": user_id, "timestamp": "..."}
        """
        # Accept the WebSocket connection
        # Roman Urdu: WebSocket connection accept karna
        await websocket.accept()
        
        # Add to active connections
        # Roman Urdu: Active connections mein add karna
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        
        # Send connection confirmation
        # Roman Urdu: Connection confirmation bhejna
        await websocket.send_json({
            "type": "connected",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    async def disconnect(self, websocket: WebSocket, user_id: int) -> None:
        """
        Remove WebSocket connection from tracking
        
        Roman Urdu: WebSocket connection ko tracking se remove karta hai
        
        Args:
            websocket: WebSocket connection object to remove
            user_id: User ka ID jiska connection tha
        """
        # Remove from active connections
        # Roman Urdu: Active connections se remove karna
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            
            # If no more connections for this user, remove the user
            # Roman Urdu: Agar koi connection nahi bacha toh user ko bhi remove karna
            if len(self.active_connections[user_id]) == 0:
                del self.active_connections[user_id]
    
    async def broadcast_to_user(self, user_id: int, message: dict) -> None:
        """
        Broadcast message to all connections of a user
        
        Roman Urdu: User ke saare connected tabs/devices ko message bhejta hai
        
        Args:
            user_id: User ka ID jisko message bhejna hai
            message: Message dictionary (must be JSON serializable)
        
        Example:
            await manager.broadcast_to_user(
                user_id=1,
                message={
                    "type": "task.updated",
                    "data": {"id": 1, "title": "Updated task", "status": "completed"}
                }
            )
        
        Handles:
            - Disconnected sockets gracefully
            - Multiple connections per user
            - Message serialization errors
        """
        # Get all connections for this user
        # Roman Urdu: User ke saare connections obtain karna
        if user_id not in self.active_connections:
            return
        
        connections = self.active_connections[user_id].copy()
        
        # Send to all connections
        # Roman Urdu: Saare connections ko message bhejna
        for websocket in connections:
            try:
                await websocket.send_json(message)
            except Exception as e:
                # Connection might be closed, ignore error
                # Roman Urdu: Agar connection closed hai toh error ignore karna
                print(f"Failed to send message to WebSocket: {e}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket) -> None:
        """
        Send message to a specific WebSocket connection
        
        Roman Urdu: Specific WebSocket connection ko message bhejta hai
        
        Args:
            message: Message dictionary
            websocket: Target WebSocket connection
        """
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Failed to send personal message: {e}")
    
    def get_connection_count(self, user_id: int) -> int:
        """
        Get number of active connections for a user
        
        Roman Urdu: User ke active connections ki ginti return karta hai
        
        Args:
            user_id: User ka ID
        
        Returns:
            Number of active WebSocket connections
        """
        if user_id not in self.active_connections:
            return 0
        return len(self.active_connections[user_id])


# Global connection manager instance
# Roman Urdu: Global connection manager instance - pure application mein use hoga
manager = ConnectionManager()


async def get_websocket_manager() -> ConnectionManager:
    """
    Dependency to get WebSocket manager instance
    
    Roman Urdu: WebSocket manager instance obtain karne ke liye dependency
    
    Returns:
        ConnectionManager instance
    """
    return manager


async def authenticate_websocket(websocket: WebSocket) -> int:
    """
    Authenticate WebSocket connection using JWT token
    
    Roman Urdu: WebSocket connection ko JWT token se authenticate karta hai
    
    Args:
        websocket: WebSocket connection with token query parameter
    
    Returns:
        user_id: Authenticated user ka ID
    
    Raises:
        WebSocketDisconnect: If authentication fails
    
    Query Parameter:
        token: JWT access token
    
    Error Codes:
        4001: Invalid or expired token
        4002: Missing token
    """
    # Get token from query parameters
    # Roman Urdu: Query parameters se token obtain karna
    token = websocket.query_params.get("token")
    
    if not token:
        # Missing token
        # Roman Urdu: Token missing hai
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect(code=4002, reason="Missing authentication token")
    
    try:
        # Verify token
        # Roman Urdu: Token verify karna
        token_data: TokenData = verify_token(token)
        
        if not token_data or not token_data.email:
            raise WebSocketDisconnect(code=4001, reason="Invalid token")
        
        # Import User model here to avoid circular import
        # Roman Urdu: Circular import se bachne ke liye yahan import karna
        from app.database import get_db
        from app.models import User
        from sqlalchemy.orm import Session
        
        # Get user from database
        # Roman Urdu: Database se user obtain karna
        db: Session = next(get_db())
        user = db.query(User).filter(User.email == token_data.email).first()
        db.close()
        
        if not user:
            raise WebSocketDisconnect(code=4001, reason="User not found")
        
        return user.id
    
    except Exception as e:
        # Authentication failed
        # Roman Urdu: Authentication failed
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketDisconnect(code=4001, reason=f"Authentication failed: {str(e)}")
