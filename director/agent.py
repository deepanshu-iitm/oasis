"""Deterministic coordinator for the first director workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from director.schema import Brand, VideoPlan
from director.tools.critique_plan import critique_plan
from director.tools.map_assets import map_assets
from director.tools.parse_brief import parse_brief
from director.tools.propose_beats import propose_beats
from director.tools.write_outputs import write_outputs


@dataclass
class DirectorResult:
    """Artifacts created by one director run."""

    plan: VideoPlan
    critique: dict[str, object]
    plan_path: Path
    storyboard_path: Path


def run_director(
    brief: str,
    out_dir: str | Path,
    *,
    duration_sec: int = 20,
    screenshot_paths: list[str] | None = None,
    on_step: Callable[[str], None] | None = None,
) -> DirectorResult:
    """Create and save a deterministic video plan from a product brief."""
    if on_step:
        on_step("parse_brief")
    parsed = parse_brief(brief)

    if on_step:
        on_step("propose_beats")
    beats = propose_beats(parsed, duration_sec)

    if on_step:
        on_step("map_assets")
    beats = map_assets(beats, screenshot_paths)

    brand_name = str(parsed["title"]).split(maxsplit=1)[0].rstrip(".,!?")
    plan = VideoPlan(
        title=str(parsed["title"]),
        brand=Brand(name=brand_name, cta_url="https://example.com"),
        beats=beats,
        duration_sec=duration_sec,
    )

    if on_step:
        on_step("critique_plan")
    critique = critique_plan(plan)

    if on_step:
        on_step("write_outputs")
    plan_path, storyboard_path = write_outputs(plan, out_dir)
    return DirectorResult(plan, critique, plan_path, storyboard_path)