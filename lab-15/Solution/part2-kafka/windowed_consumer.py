"""Additional Kafka consumer that groups orders into time-based metrics windows."""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from kafka import KafkaConsumer

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] - %(message)s")
logger = logging.getLogger(__name__)


class WindowedMetricConsumer:
    def __init__(
        self,
        bootstrap_servers: str = "localhost:9092",
        topic: str = "orders",
        window_size_seconds: int = 30,
        group_id: str = "filipov_window_group",
    ):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.window_size_seconds = window_size_seconds
        self.group_id = group_id
        self.consumer: KafkaConsumer | None = None
        self.snapshots_list: list[dict] = []

    def start_kafka_listener(self) -> None:
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
            consumer_timeout_ms=10000,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        logger.info("[KAFKA-WINDOWED] Listening to topic %s", self.topic)

    def run(self, max_messages: int | None = 15) -> None:
        self.start_kafka_listener()
        assert self.consumer is not None
        window_start_time = datetime.now()
        active_window_data = {"orders": 0, "sales": 0.0, "category_sales": defaultdict(int)}
        processed = 0

        try:
            for message in self.consumer:
                order = message.value
                current_time = datetime.now()
                if current_time - window_start_time >= timedelta(seconds=self.window_size_seconds):
                    self.snapshots_list.append(self._take_snapshot(window_start_time, current_time, active_window_data))
                    window_start_time = current_time
                    active_window_data = {"orders": 0, "sales": 0.0, "category_sales": defaultdict(int)}

                active_window_data["orders"] += 1
                active_window_data["sales"] += float(order["total_amount"])
                for item in order["items"]:
                    active_window_data["category_sales"][item["category"]] += item["quantity"]

                processed += 1
                if max_messages is not None and processed >= max_messages:
                    break
        finally:
            self.snapshots_list.append(self._take_snapshot(window_start_time, datetime.now(), active_window_data))
            self.consumer.close()
            output_file = DATA_DIR / "windowed_metrics_output.json"
            output_file.write_text(
                json.dumps(self.snapshots_list, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            logger.info("[KAFKA-WINDOWED] Saved %s metrics snapshots to %s", len(self.snapshots_list), output_file)

    @staticmethod
    def _take_snapshot(start: datetime, end: datetime, data: dict) -> dict:
        return {
            "window_started": start.isoformat(),
            "window_finished": end.isoformat(),
            "orders_processed": data["orders"],
            "total_sales_value": data["sales"],
            "categories_sales_qty": dict(data["category_sales"]),
        }


if __name__ == "__main__":
    WindowedMetricConsumer().run()
