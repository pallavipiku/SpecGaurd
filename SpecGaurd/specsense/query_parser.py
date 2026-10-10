from __future__ import annotations

import re


def _detect_category(text: str) -> str | None:
    categories = {
        "laptop": ["laptop", "notebook", "ultrabook"],
        "mobile": ["mobile", "phone", "smartphone"],
        "headphones": ["headphone", "earphone", "earbuds"],
        "camera": ["camera", "dslr", "mirrorless"],
        "watch": ["watch", "smartwatch"],
    }

    for category, keywords in categories.items():
        if any(keyword in text for keyword in keywords):
            return category
    return None


def _extract_budget(text: str) -> float | None:
    patterns = [
        r"(?:under|below|upto|up to|within|max(?:imum)?|less than|budget(?:\s+of)?(?:\s+under)?)\s*(?:₹\s*)?(\d+(?:,\d{3})*(?:\.\d+)?)",
        r"(?:₹\s*)(\d+(?:,\d{3})*(?:\.\d+)?)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = match.group(1).replace(",", "")
            try:
                return float(value)
            except ValueError:
                continue
    return None


def _extract_soft_preferences(text: str) -> list[str]:
    preferences = []
    preference_map = {
        "lightweight": ["lightweight", "portable", "travel-friendly", "travel friendly", "easy to carry"],
        "battery life": ["battery life", "battery backup", "long battery", "good battery", "lasting battery"],
        "coding": ["coding", "programming", "developer", "software development"],
        "performance": ["performance", "fast", "smooth", "powerful"],
        "camera quality": ["camera quality", "good camera", "sharp camera", "photo quality"],
        "durability": ["durable", "robust", "long lasting"],
    }

    for label, keywords in preference_map.items():
        if any(keyword in text for keyword in keywords):
            preferences.append(label)

    return preferences


def parse_query(query: str) -> dict:
    """Extract category, budget and soft preferences from a free-form query."""
    clean = query.lower().strip()
    return {
        "category": _detect_category(clean),
        "budget": _extract_budget(clean),
        "soft_preferences": _extract_soft_preferences(clean),
        "raw_query": query,
    }
