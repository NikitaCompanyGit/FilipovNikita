"""Kafka consumer that aggregates order statistics."""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from kafka import KafkaConsumer

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)


class SalesReportingConsumer:
    def __init__(self, bootstrap_servers: str = "localhost:9092", topic: str = "orders", group_id: str = "filipov_analytics_group"):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer: KafkaConsumer | None = None
        self.metrics = {
            "total_orders_received": 0,
            "accumulated_sales_volume": 0.0,
            "category_distribution": defaultdict(int),
            "city_distribution": defaultdict(int),
            "last_orders": [],
            "initialized_at": datetime.now().isoformat(),
        }

    def start_kafka_consumer(self) -> None:
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            consumer_timeout_ms=10000,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            key_deserializer=lambda k: k.decode("utf-8") if k else None,
        )
        logger.info("[KAFKA-CONSUMER] Subscribed to topic: %s", self.topic)

    def consume_order_event(self, order: dict) -> None:
        self.metrics["total_orders_received"] += 1
        self.metrics["accumulated_sales_volume"] += float(order["total_amount"])
        for item in order["items"]:
            self.metrics["category_distribution"][item["category"]] += 1
        self.metrics["city_distribution"][order["customer"]["city"]] += 1
        self.metrics["last_orders"].append(
            {
                "order_id": order["order_id"],
                "buyer": order["customer"]["name"],
                "value": order["total_amount"],
                "timestamp": order["timestamp"],
            }
        )
        self.metrics["last_orders"] = self.metrics["last_orders"][-10:]

    def build_report_data(self) -> dict:
        return {
            **self.metrics,
            "category_distribution": dict(self.metrics["category_distribution"]),
            "city_distribution": dict(self.metrics["city_distribution"]),
        }

    def save_metrics_report(self) -> None:
        report_file = DATA_DIR / "sales_analytics_report.json"
        report_file.write_text(
            json.dumps(self.build_report_data(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        logger.info("[KAFKA-CONSUMER] Saved metrics report to %s", report_file)

    def run(self, max_messages: int | None = None) -> None:
        self.start_kafka_consumer()
        assert self.consumer is not None
        processed = 0
        try:
            for message in self.consumer:
                self.consume_order_event(message.value)
                processed += 1
                logger.info("[KAFKA-CONSUMER] Consumed event: %s", message.value["order_id"])
                if max_messages is not None and processed >= max_messages:
                    break
        finally:
            self.consumer.close()
            self.save_metrics_report()
            logger.info("[KAFKA-CONSUMER] Final stats: %s", self.build_report_data())


if __name__ == "__main__":
    SalesReportingConsumer().run(max_messages=15)
