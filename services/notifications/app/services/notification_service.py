"""
Sanos y Salvos — Notification Service
Processes match events and generates user notifications.
"""

import logging
from datetime import datetime
from typing import List

from app.websocket.manager import manager

logger = logging.getLogger("notification_service")

# In-memory notification store (for demo; in production use a database)
notifications_store: List[dict] = []


class NotificationService:
    """Handles notification creation and delivery."""

    @staticmethod
    async def create_notification(match_data: dict):
        """
        Create and send a notification when a match is found.
        """
        notification = {
            "id": len(notifications_store) + 1,
            "type": "match_found",
            "title": "¡Posible coincidencia encontrada!",
            "message": (
                f"Se ha encontrado una posible coincidencia con un score de "
                f"{match_data.get('score', 0):.0f}%"
            ),
            "match_id": match_data.get("_id"),
            "score": match_data.get("score", 0),
            "report_lost_id": match_data.get("report_lost_id"),
            "report_found_id": match_data.get("report_found_id"),
            "pet_lost_name": match_data.get("pet_lost_name", "Desconocido"),
            "pet_found_name": match_data.get("pet_found_name", "Desconocido"),
            "read": False,
            "created_at": datetime.utcnow().isoformat(),
        }

        notifications_store.append(notification)
        logger.info(f"🔔 Notification created: {notification['title']}")

        # Send via WebSocket to specific users
        user_lost_id = str(match_data.get("user_lost_id", ""))
        user_found_id = str(match_data.get("user_found_id", ""))

        if user_lost_id:
            await manager.send_to_user(user_lost_id, notification)
        if user_found_id:
            await manager.send_to_user(user_found_id, notification)

        # Broadcast to all connected clients (dashboard)
        await manager.broadcast(notification)

        return notification

    @staticmethod
    def get_notifications(user_id: str = None, limit: int = 50) -> List[dict]:
        """Get notifications, optionally filtered by user."""
        results = sorted(notifications_store, key=lambda x: x["created_at"], reverse=True)
        return results[:limit]

    @staticmethod
    def mark_as_read(notification_id: int) -> bool:
        for n in notifications_store:
            if n["id"] == notification_id:
                n["read"] = True
                return True
        return False

    @staticmethod
    def get_unread_count() -> int:
        return sum(1 for n in notifications_store if not n["read"])
