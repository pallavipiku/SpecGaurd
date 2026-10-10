from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def _coerce_numeric(value: Any) -> float | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).replace(",", "").replace("₹", "").replace(" ", "")
    try:
        return float(text)
    except ValueError:
        return None


def load_products(csv_path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load product catalog from CSV and normalize fields."""
    if csv_path is None:
        csv_path = Path(__file__).resolve().parents[1] / "data" / "sample_products.csv"

    df = pd.read_csv(csv_path)
    normalized_rows: list[dict[str, Any]] = []

    for _, row in df.iterrows():
        item = row.to_dict()
        item["price"] = _coerce_numeric(item.get("price"))
        item["weight_kg"] = _coerce_numeric(item.get("weight_kg"))
        item["ram_gb"] = _coerce_numeric(item.get("ram_gb"))
        item["storage_gb"] = _coerce_numeric(item.get("storage_gb"))
        item["battery_ah"] = _coerce_numeric(item.get("battery_ah"))
        item["category"] = str(item.get("category", "")).strip().lower()
        item["product_name"] = str(item.get("product_name", "")).strip()
        normalized_rows.append(item)

    return normalized_rows
