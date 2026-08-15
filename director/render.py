"""Bridge a Python video plan to the local Remotion renderer."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from director.schema import VideoPlan


COMPOSITION_ID = "DirectorReel"


def render_video(plan: VideoPlan, out_dir: str | Path) -> Path:
    """Render a ``VideoPlan`` to ``final.mp4`` using the local Remotion app."""
    output_dir = Path(out_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    props_path = output_dir / "remotion-props.json"
    output_path = output_dir / "final.mp4"
    props_path.write_text(
        json.dumps(_remotion_props(plan), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    project_root = Path(__file__).resolve().parents[1]
    remotion_dir = project_root / "remotion"
    remotion_binary = remotion_dir / "node_modules" / ".bin" / "remotion.cmd"
    if not remotion_binary.is_file():
        raise FileNotFoundError(
            "Remotion is not installed. Run `npm install` in the remotion directory first."
        )

    subprocess.run(
        [
            str(remotion_binary),
            "render",
            "src/index.ts",
            COMPOSITION_ID,
            str(output_path),
            f"--props={props_path}",
        ],
        cwd=remotion_dir,
        check=True,
    )
    return output_path


def _remotion_props(plan: VideoPlan) -> dict[str, object]:
    return {
        "accentColor": plan.brand.accent,
        "brandName": plan.brand.name,
        "beats": [
            {
                "id": beat.id,
                "caption_heading": beat.caption_heading,
                "caption_desc": beat.caption_desc,
                "duration_sec": beat.duration_sec,
            }
            for beat in plan.beats
        ],
    }