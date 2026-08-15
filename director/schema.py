"""Stable, renderer-facing data structures for a directed video."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Brand:
    """Brand details shared by all video beats."""

    name: str
    accent: str = "#2D5BFF"
    cta_url: str = ""


@dataclass
class Beat:
    """One timed segment in the video production plan."""

    id: str
    intent: str
    scene_type: str
    spoken: str
    caption_heading: str
    caption_desc: str
    visual: str
    duration_sec: float
    asset_refs: list[str] = field(default_factory=list)


@dataclass
class VideoPlan:
    """The complete plan consumed by the storyboard writer and renderer."""

    title: str
    brand: Brand
    beats: list[Beat]
    format: str = "9:16"
    duration_sec: float = 20
    fps: int = 30
    music_mood: str = "tech"
    selected_engine: str = "motion"

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of this plan."""
        return asdict(self)