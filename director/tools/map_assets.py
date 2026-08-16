"""Attach optional screenshot assets to the most relevant video beats."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from director.schema import Beat


ASSET_BEAT_INTENTS = {"product", "proof"}


def map_assets(beats: list[Beat], screenshot_paths: list[str] | None = None) -> list[Beat]:
    """Map up to one screenshot onto each product or proof beat.

    Paths are preserved as renderer-facing strings. File validation happens at
    render time so the planner can also work with assets supplied later.
    """
    asset_paths = [str(Path(path)) for path in screenshot_paths or []]
    asset_index = 0
    mapped_beats: list[Beat] = []

    for beat in beats:
        if beat.intent in ASSET_BEAT_INTENTS and asset_index < len(asset_paths):
            mapped_beats.append(replace(beat, asset_refs=[asset_paths[asset_index]]))
            asset_index += 1
        else:
            mapped_beats.append(replace(beat, asset_refs=[]))

    return mapped_beats