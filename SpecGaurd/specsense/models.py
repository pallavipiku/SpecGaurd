from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class ProductRecord(BaseModel):
    """Structured product model used across the recommendation flow."""

    product_id: str
    product_name: str
    category: str
    price: float
    brand: Optional[str] = None
    weight_kg: Optional[float] = None
    ram_gb: Optional[float] = None
    storage_gb: Optional[float] = None
    battery_ah: Optional[float] = None
    processor: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(extra="allow")


class QueryIntent(BaseModel):
    """Structured output for a user product query."""

    category: Optional[str] = None
    budget: Optional[float] = None
    soft_preferences: list[str] = []
    raw_query: str = ""


class RecommendationResult(BaseModel):
    """Final recommendation item returned to the UI."""

    product_id: str
    product_name: str
    category: str
    price: float
    score: float
    matched_hard_constraints: list[str]
    soft_matches: list[str]
    unmet_requirements: list[str]
    trade_offs: list[str]
    recommendation_reason: str
    product_snapshot: dict[str, Any]
