"""Write a video plan in machine-readable and presenter-friendly formats."""

from __future__ import annotations

import json
from pathlib import Path

from director.schema import VideoPlan


def write_outputs(plan: VideoPlan, out_dir: str | Path) -> tuple[Path, Path]:
    """Write ``plan.json`` and ``storyboard.md`` and return their paths."""
    output_path = Path(out_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    plan_path = output_path / "plan.json"
    plan_path.write_text(
        json.dumps(plan.to_dict(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    storyboard_path = output_path / "storyboard.md"
    storyboard_path.write_text(_storyboard_markdown(plan), encoding="utf-8")
    return plan_path, storyboard_path


def _storyboard_markdown(plan: VideoPlan) -> str:
    lines = [
        f"# {plan.title}",
        "",
        f"**Format:** {plan.format}  ",
        f"**Duration:** {plan.duration_sec:g}s at {plan.fps} FPS  ",
        f"**Brand:** {plan.brand.name}  ",
        f"**Music mood:** {plan.music_mood}",
        "",
        "## Beats",
        "",
    ]

    for beat in plan.beats:
        lines.extend(
            [
                f"### {beat.id.upper()} - {beat.intent.title()} ({beat.duration_sec:g}s)",
                "",
                f"**On screen:** {beat.caption_heading}",
                beat.caption_desc,
                "",
                f"**Spoken:** {beat.spoken}",
                "",
                f"**Visual direction:** {beat.visual}",
                "",
                f"**Assets:** {', '.join(beat.asset_refs) if beat.asset_refs else 'Kinetic text'}",
                "",
            ]
        )

    return "\n".join(lines)