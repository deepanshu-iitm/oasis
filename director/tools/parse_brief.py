"""Convert a raw product brief into structured planning inputs."""

from __future__ import annotations

import re


def parse_brief(text: str) -> dict[str, object]:
    """Extract a small, predictable brief summary without an LLM.

    This deterministic fallback keeps the first pipeline step usable before the
    LLM-backed director is added.
    """
    normalized = " ".join(text.split())
    if not normalized:
        raise ValueError("A product brief cannot be empty.")

    sentences = re.split(r"(?<=[.!?])\s+", normalized)
    product = sentences[0]
    title = product[:60].rstrip(". !?")

    return {
        "title": title,
        "product": product,
        "audience": "people who would benefit from this product",
        "cta": "Learn more",
        "constraints": [],
    }