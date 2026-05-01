"""
Sanos y Salvos — RabbitMQ Event Publisher
Publishes events when pets are reported (lost/found).
"""

import json
import logging
import aio_pika
from typing import Optional

from app.config import RABBITMQ_URL

logger = logging.getLogger("events.publisher")

EXCHANGE_NAME = "sanos_y_salvos"
ROUTING_KEY_PET_REPORTED = "pet.reported"


class EventPublisher:
    """Publishes domain events to RabbitMQ."""

    def __init__(self):
        self._connection: Optional[aio_pika.Connection] = None
        self._channel: Optional[aio_pika.Channel] = None

    async def connect(self):
        """Establish connection to RabbitMQ."""
        try:
            self._connection = await aio_pika.connect_robust(RABBITMQ_URL)
            self._channel = await self._connection.channel()
            # Declare topic exchange
            await self._channel.declare_exchange(
                EXCHANGE_NAME, aio_pika.ExchangeType.TOPIC, durable=True
            )
            logger.info("✅ Connected to RabbitMQ (Publisher)")
        except Exception as e:
            logger.error(f"❌ Failed to connect to RabbitMQ: {e}")

    async def publish_pet_reported(self, report_data: dict):
        """
        Publish 'pet.reported' event when a new report is created.
        The Match service and Notifications service will consume this event.
        """
        if not self._channel:
            logger.warning("RabbitMQ not connected. Attempting reconnect...")
            await self.connect()

        try:
            exchange = await self._channel.get_exchange(EXCHANGE_NAME)
            message = aio_pika.Message(
                body=json.dumps(report_data, default=str).encode(),
                content_type="application/json",
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )
            await exchange.publish(message, routing_key=ROUTING_KEY_PET_REPORTED)
            logger.info(f"📤 Event published: {ROUTING_KEY_PET_REPORTED} — Report #{report_data.get('report_id')}")
        except Exception as e:
            logger.error(f"❌ Failed to publish event: {e}")

    async def close(self):
        """Close RabbitMQ connection."""
        if self._connection:
            await self._connection.close()
            logger.info("RabbitMQ connection closed")


# Singleton publisher instance
publisher = EventPublisher()
