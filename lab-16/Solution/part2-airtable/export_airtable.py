"""Export Airtable CRM tables to CSV files using real API credentials (refactored for Nikita)."""

from __future__ import annotations

import csv
import os
from pathlib import Path

import requests
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
EXPORT_DIR = BASE_DIR / "exported_data"
TARGET_TABLES = ["Customers", "Products", "Orders", "Order Items"]


def get_env_config() -> tuple[str, str]:
    load_dotenv(BASE_DIR / ".env")
    token = os.getenv("AIRTABLE_TOKEN", "").strip()
    base_id = os.getenv("AIRTABLE_BASE_ID", "").strip()
    if not token or not base_id:
        raise RuntimeError("AIRTABLE_TOKEN and AIRTABLE_BASE_ID must be set in your .env file")
    return token, base_id


def download_airtable_records(auth_token: str, app_base_id: str, table_title: str) -> list[dict]:
    records: list[dict] = []
    offset_token: str | None = None
    headers = {"Authorization": f"Bearer {auth_token}"}
    while True:
        query_params = {"pageSize": 100}
        if offset_token:
            query_params["offset"] = offset_token
        response = requests.get(
            f"https://api.airtable.com/v0/{app_base_id}/{table_title}",
            headers=headers,
            params=query_params,
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        records.extend(payload.get("records", []))
        offset_token = payload.get("offset")
        if not offset_token:
            return records


def save_records_to_csv(table_title: str, records: list[dict]) -> Path:
    EXPORT_DIR.mkdir(exist_ok=True)
    all_keys = sorted({key for rec in records for key in rec.get("fields", {}).keys()})
    dest_path = EXPORT_DIR / f"{table_title.replace(' ', '_').lower()}_sheet.csv"
    with dest_path.open("w", encoding="utf-8", newline="") as output_file:
        csv_writer = csv.DictWriter(output_file, fieldnames=["id", *all_keys])
        csv_writer.writeheader()
        for rec in records:
            row_data = {"id": rec["id"], **rec.get("fields", {})}
            csv_writer.writerow(row_data)
    return dest_path


def execute_export() -> None:
    try:
        auth_token, app_base_id = get_env_config()
        for table in TARGET_TABLES:
            records = download_airtable_records(auth_token, app_base_id, table)
            csv_path = save_records_to_csv(table, records)
            print(f"Exported {len(records)} records from {table} to {csv_path.name}")
    except Exception as err:
        print(f"Export aborted: {err}")


if __name__ == "__main__":
    execute_export()
