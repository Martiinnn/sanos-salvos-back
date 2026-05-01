"""
Sanos y Salvos — Notifications API Routes
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query

from app.services.notification_service import NotificationService
from app.websocket.manager import manager

router = APIRouter(prefix="/api/notifications", tags=["Notificaciones"])


@router.get("/")
def list_notifications(limit: int = Query(50, ge=1, le=100)):
    """Get recent notifications."""
    return NotificationService.get_notifications(limit=limit)


@router.get("/unread-count")
def unread_count():
    """Get number of unread notifications."""
    return {"count": NotificationService.get_unread_count()}


@router.patch("/{notification_id}/read")
def mark_read(notification_id: int):
    """Mark a notification as read."""
    success = NotificationService.mark_as_read(notification_id)
    if success:
        return {"message": "Marcada como leída"}
    return {"message": "Notificación no encontrada"}


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time notifications."""
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Keep connection alive, listen for client messages
            data = await websocket.receive_text()
            # Echo back for ping/pong
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)


@router.websocket("/ws")
async def websocket_broadcast(websocket: WebSocket):
    """WebSocket endpoint for broadcast notifications (dashboard)."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
