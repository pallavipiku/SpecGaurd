from __future__ import annotations

from typing import Any

from .data_loader import load_products
from .matcher import match_products
from .query_parser import parse_query


def generate_recommendations(query: str, products: list[dict[str, Any]] | None = None, top_n: int = 5) -> dict[str, Any]:
    """Generate ranked recommendations for a user query."""
    parsed = parse_query(query)
    catalog = products if products is not None else load_products()
    recommendations = match_products(catalog, parsed)
    return {
        "intent": parsed,
        "recommendations": recommendations[:top_n],
    }
