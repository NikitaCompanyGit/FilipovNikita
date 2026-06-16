"""Kafka producer that generates shop order events."""

from __future__ import annotations

import json
import logging
import random
import time
import uuid
from datetime import datetime

from kafka import KafkaProducer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)


class OrderStreamingProducer:
    def __init__(self, bootstrap_servers: str = "localhost:9092", topic: str = "orders"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer: KafkaProducer | None = None

    def open_producer_connection(self) -> None:
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode("utf-8"),
            key_serializer=lambda k: k.encode("utf-8") if k else None,
        )
        logger.info("[KAFKA-STREAM] Connected to broker: %s", self.bootstrap_servers)

    def build_random_order_event(self) -> dict:
        catalog = [
            {"product_id": 101, "name": "Ноутбук", "price": 75000, "category": "Электроника"},
            {"product_id": 102, "name": "Мышь", "price": 1500, "category": "Электроника"},
            {"product_id": 103, "name": "Книга SQL", "price": 2500, "category": "Книги"},
            {"product_id": 104, "name": "Клавиатура", "price": 5000, "category": "Электроника"},
            {"product_id": 105, "name": "Монитор", "price": 25000, "category": "Электроника"},
            {"product_id": 106, "name": "Книга Python", "price": 3500, "category": "Книги"},
        ]
        customers = [
            {"id": 1, "name": "Никита Филиппов", "city": "Владивосток"},
            {"id": 2, "name": "Петр Иванов", "city": "Санкт-Петербург"},
            {"id": 3, "name": "Мария Сидорова", "city": "Казань"},
            {"id": 4, "name": "Иван Петров", "city": "Москва"},
            {"id": 5, "name": "Елена Козлова", "city": "Новосибирск"},
        ]
        prod = random.choice(catalog)
        cust = random.choice(customers)
        qty = random.randint(1, 3)
        return {
            "order_id": str(uuid.uuid4())[:8],
            "timestamp": datetime.now().isoformat(),
            "customer": cust,
            "items": [
                {
                    "product_id": prod["product_id"],
                    "product_name": prod["name"],
                    "category": prod["category"],
                    "quantity": qty,
                    "unit_price": prod["price"],
                    "total_price": qty * prod["price"],
                }
            ],
            "total_amount": qty * prod["price"],
            "payment_method": random.choice(["card", "cash", "online"]),
        }

    def stream_order_event(self, order: dict):
        if self.producer is None:
            raise RuntimeError("Must call open_producer_connection() before streaming events")
        partition_key = str(order["customer"]["id"])
        future = self.producer.send(self.topic, key=partition_key, value=order)
        meta = future.get(timeout=10)
        logger.info("[KAFKA-STREAM] Dispatched order: %s to partition: %s at offset: %s", order["order_id"], meta.partition, meta.offset)
        return future

    def run(self, interval_seconds: float = 1.0, max_orders: int = 15) -> None:
        self.open_producer_connection()
        for _ in range(max_orders):
            self.stream_order_event(self.build_random_order_event())
            time.sleep(interval_seconds)
        assert self.producer is not None
        self.producer.flush()
        self.producer.close()
        logger.info("[KAFKA-STREAM] Event generation complete.")


if __name__ == "__main__":
    OrderStreamingProducer().run()
