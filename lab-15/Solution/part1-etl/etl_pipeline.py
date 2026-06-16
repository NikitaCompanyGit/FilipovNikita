"""ETL pipeline for shop sales analytics."""

from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
GRAPH_DIR = BASE_DIR / "report" / "graphs"
LOG_DIR.mkdir(exist_ok=True)
GRAPH_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "etl_process.log", encoding="utf-8", mode="w"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class SalesDataPipeline:
    """Extract, Transform, Aggregate, Load and Visualize sales dataset."""

    def __init__(self, input_csv: str | Path, output_db: str | Path = "sales_analytics.db"):
        self.input_csv = Path(input_csv)
        self.output_db = Path(output_db)
        self.raw_df: pd.DataFrame | None = None
        self.cleaned_df: pd.DataFrame | None = None
        self.aggregated_df: pd.DataFrame | None = None

    def retrieve_raw_csv(self) -> pd.DataFrame:
        logger.info("[ETL-PROCESS] Extracting raw CSV data")
        if not self.input_csv.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_csv}")

        self.raw_df = pd.read_csv(self.input_csv)
        if self.raw_df.empty:
            raise ValueError("CSV dataset is empty")

        logger.info("[ETL-PROCESS] Loaded %s entries", len(self.raw_df))
        return self.raw_df

    def validate_and_transform(self) -> pd.DataFrame:
        logger.info("[ETL-PROCESS] Transforming raw dataset")
        if self.raw_df is None:
            raise RuntimeError("Extraction must be run before transformation")

        df = self.raw_df.copy()
        row_count_before = len(df)
        df = df.drop_duplicates()
        logger.info("[ETL-PROCESS] Removed %s duplicate records", row_count_before - len(df))

        # Валидация числовых значений
        num_fields = ["quantity", "price_per_unit"]
        for field in num_fields:
            df[field] = pd.to_numeric(df[field], errors="coerce")
            df[field] = df[field].fillna(df[field].median())

        # Заполнение текстовых пропусков
        str_fields = ["product_name", "category", "customer_name", "customer_city", "payment_method"]
        for field in str_fields:
            df[field] = df[field].fillna("NotAvailable").replace("", "NotAvailable")

        # Парсинг временных меток
        df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
        df = df.dropna(subset=["order_date"])

        # Фильтрация некорректных значений
        df = df[(df["quantity"] > 0) & (df["price_per_unit"] > 0)]
        df["quantity"] = df["quantity"].astype(int)
        df["total_amount"] = df["quantity"] * df["price_per_unit"]
        df["month_year"] = df["order_date"].dt.to_period("M").astype(str)

        self.cleaned_df = df
        logger.info("[ETL-PROCESS] Rows after validation/cleaning: %s", len(df))
        return df

    def compute_aggregates(self) -> pd.DataFrame:
        logger.info("[ETL-PROCESS] Aggregating sales metrics")
        if self.cleaned_df is None:
            raise RuntimeError("Transformation must be run before aggregation")

        self.aggregated_df = (
            self.cleaned_df.groupby(["category", "month_year"], as_index=False)
            .agg(
                total_qty=("quantity", "sum"),
                total_revenue=("total_amount", "sum"),
                avg_unit_price=("price_per_unit", "mean"),
                distinct_orders=("order_id", "nunique"),
            )
            .sort_values(["month_year", "total_revenue"], ascending=[True, False])
        )
        logger.info("[ETL-PROCESS] Generated %s unique aggregates", len(self.aggregated_df))
        return self.aggregated_df

    def load_to_sqlite(self) -> None:
        logger.info("[ETL-PROCESS] Loading processed tables to SQLite")
        if self.cleaned_df is None or self.aggregated_df is None:
            raise RuntimeError("Transformation and aggregation must run before loading")

        with sqlite3.connect(self.output_db) as conn:
            self.cleaned_df.to_sql("cleaned_sales_data", conn, if_exists="replace", index=False)
            self.aggregated_df.to_sql("aggregated_sales_report", conn, if_exists="replace", index=False)
        logger.info("[ETL-PROCESS] Saved processed tables to SQLite: %s", self.output_db)

    def create_charts(self) -> None:
        logger.info("[ETL-PROCESS] Generating analytical charts")
        if self.cleaned_df is None or self.aggregated_df is None:
            raise RuntimeError("Transformation and aggregation must run before visualization")

        grouped_rev = (
            self.cleaned_df.groupby("category", as_index=False)["total_amount"]
            .sum()
            .sort_values("total_amount", ascending=False)
        )
        
        # Столбчатая диаграмма доходов по категориям
        plt.figure(figsize=(9, 5))
        plt.bar(grouped_rev["category"], grouped_rev["total_amount"], color="darkorange")
        plt.title("Доходы по товарным категориям")
        plt.xlabel("Категории")
        plt.ylabel("Доход")
        plt.tight_layout()
        plt.savefig(GRAPH_DIR / "revenue_by_category.png", dpi=140)
        plt.close()

        # Линейный график ежемесячной выручки
        monthly = self.cleaned_df.groupby("month_year", as_index=False)["total_amount"].sum()
        plt.figure(figsize=(9, 5))
        plt.plot(monthly["month_year"], monthly["total_amount"], marker="o", color="navy")
        plt.title("Выручка по месяцам")
        plt.xlabel("Месяц")
        plt.ylabel("Выручка")
        plt.tight_layout()
        plt.savefig(GRAPH_DIR / "monthly_revenue.png", dpi=140)
        plt.close()

        # Круговая диаграмма долей категорий
        plt.figure(figsize=(7, 7))
        plt.pie(grouped_rev["total_amount"], labels=grouped_rev["category"], autopct="%1.1f%%", startangle=90)
        plt.title("Доли товарных категорий")
        plt.tight_layout()
        plt.savefig(GRAPH_DIR / "category_share.png", dpi=140)
        plt.close()
        logger.info("[ETL-PROCESS] Charts generated and saved in %s", GRAPH_DIR)

    def run(self) -> None:
        logger.info("=" * 60)
        logger.info("SalesDataPipeline started")
        logger.info("=" * 60)
        self.retrieve_raw_csv()
        self.validate_and_transform()
        self.compute_aggregates()
        self.load_to_sqlite()
        self.create_charts()
        logger.info("SalesDataPipeline finished")


if __name__ == "__main__":
    pipeline = SalesDataPipeline(
        input_csv=BASE_DIR / "data" / "sales.csv",
        output_db=BASE_DIR / "sales_analytics.db"
    )
    pipeline.run()
