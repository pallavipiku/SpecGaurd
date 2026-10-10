from __future__ import annotations

from typing import Any


def _safe_float(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _soft_match(product: dict[str, Any], preference: str) -> tuple[bool, float, str]:
    """Return (matched, score, reason_text)."""
    weight = _safe_float(product.get("weight_kg"))
    ram = _safe_float(product.get("ram_gb"))
    battery = _safe_float(product.get("battery_ah"))
    price = _safe_float(product.get("price"))

    if preference == "lightweight":
        if weight and weight <= 1.4:
            return True, 14, "Lightweight design fits portability needs."
        if weight and weight <= 1.8:
            return True, 8, "Moderately portable option with acceptable weight."
        return False, 0, "Weight is higher than desired for portability."

    if preference == "coding":
        if ram >= 12:
            return True, 18, "Strong RAM profile supports coding workloads."
        if ram >= 8:
            return True, 10, "Adequate RAM for basic coding and multitasking."
        return False, 0, "RAM is limited for coding-focused usage."

    if preference == "battery life":
        if battery >= 60:
            return True, 18, "Battery capacity is strong for long usage periods."
        if battery >= 45:
            return True, 9, "Battery is decent but not exceptional."
        return False, 0, "Battery capacity falls short of long-usage needs."

    if preference == "performance":
        if ram >= 12 and "i5" in str(product.get("processor", "")).lower():
            return True, 12, "Balanced processor and RAM provide good performance."
        return False, 0, "Performance profile is moderate for demanding tasks."

    if preference == "camera quality":
        if product.get("category") == "camera":
            return True, 10, "Camera category aligns with image quality needs."
        return False, 0, "No direct camera quality data is available."

    if preference == "durability":
        if price and price >= 30000:
            return True, 7, "Higher-end build may support durability expectations."
        return False, 0, "Durability signal is not well supported by available data."

    return False, 0, "Preference is not strongly evidenced in catalog data."


def match_products(products: list[dict[str, Any]], intent: dict[str, Any]) -> list[dict[str, Any]]:
    """Filter and rank products based on hard constraints and soft preferences."""
    category = (intent.get("category") or "").strip().lower()
    budget = intent.get("budget")
    soft_preferences = intent.get("soft_preferences") or []

    results: list[dict[str, Any]] = []

    for product in products:
        product = dict(product)
        product_category = str(product.get("category", "")).strip().lower()
        price = _safe_float(product.get("price"))
        weight = _safe_float(product.get("weight_kg"))
        ram = _safe_float(product.get("ram_gb"))
        battery = _safe_float(product.get("battery_ah"))

        hard_matches: list[str] = []
        unmet_requirements: list[str] = []
        soft_matches: list[str] = []
        trade_offs: list[str] = []
        score = 0.0

        if category and product_category != category:
            unmet_requirements.append(f"Category mismatch: expected {category} but found {product_category}.")
        else:
            if category:
                hard_matches.append("Category")
                score += 35

        if budget is not None:
            if price <= budget:
                hard_matches.append("Budget")
                score += 35
            else:
                unmet_requirements.append(f"Price exceeds budget: ₹{price} > ₹{budget}.")

        if category == "laptop" and ram:
            if ram >= 12:
                soft_matches.append("Strong coding performance")
                score += 12
            elif ram >= 8:
                soft_matches.append("Adequate coding performance")
                score += 8
            else:
                trade_offs.append("Limited RAM for heavier coding tasks.")

        if weight and "lightweight" in soft_preferences:
            matched, soft_score, reason = _soft_match(product, "lightweight")
            if matched:
                soft_matches.append("Lightweight")
                score += soft_score
            else:
                trade_offs.append(reason)

        if "coding" in soft_preferences:
            matched, soft_score, reason = _soft_match(product, "coding")
            if matched:
                soft_matches.append("Good for coding")
                score += soft_score
            else:
                trade_offs.append(reason)

        if "battery life" in soft_preferences:
            matched, soft_score, reason = _soft_match(product, "battery life")
            if matched:
                soft_matches.append("Long battery life")
                score += soft_score
            else:
                trade_offs.append(reason)

        if not hard_matches and category:
            unmet_requirements.append("No hard-constraint criteria matched.")

        recommendation_reason = (
            "Recommended based on strong alignment with the user’s budget and preferred product attributes."
            if soft_matches or hard_matches
            else "The catalog entry does not strongly match the stated requirements."
        )

        if not hard_matches:
            recommendation_reason = "This option does not meet the explicit conditions provided by the user."

        results.append({
            "product_id": product.get("product_id", "N/A"),
            "product_name": product.get("product_name", "Unknown"),
            "category": product.get("category", "unknown"),
            "price": price,
            "score": round(score, 2),
            "matched_hard_constraints": hard_matches,
            "soft_matches": soft_matches,
            "unmet_requirements": unmet_requirements,
            "trade_offs": trade_offs,
            "recommendation_reason": recommendation_reason,
            "product_snapshot": product,
        })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results
