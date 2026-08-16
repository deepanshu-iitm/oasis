"""OpenAI-backed planner for high-quality video production plans."""

from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from director.schema import Beat, Brand, VideoPlan


DEFAULT_MODEL = "gpt-5.6-luna"

PLAN_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "title",
        "format",
        "duration_sec",
        "fps",
        "brand",
        "beats",
        "music_mood",
        "selected_engine",
    ],
    "properties": {
        "title": {"type": "string"},
        "format": {"type": "string", "enum": ["9:16"]},
        "duration_sec": {"type": "number"},
        "fps": {"type": "integer", "enum": [30]},
        "brand": {
            "type": "object",
            "additionalProperties": False,
            "required": ["name", "accent", "cta_url"],
            "properties": {
                "name": {"type": "string"},
                "accent": {"type": "string"},
                "cta_url": {"type": "string"},
            },
        },
        "beats": {
            "type": "array",
            "minItems": 5,
            "maxItems": 5,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": [
                    "id",
                    "intent",
                    "scene_type",
                    "spoken",
                    "caption_heading",
                    "caption_desc",
                    "visual",
                    "duration_sec",
                    "asset_refs",
                ],
                "properties": {
                    "id": {"type": "string"},
                    "intent": {"type": "string", "enum": ["hook", "value", "product", "proof", "cta"]},
                    "scene_type": {
                        "type": "string",
                        "enum": ["kinetic_hook", "kinetic_point", "outro_cta"],
                    },
                    "spoken": {"type": "string"},
                    "caption_heading": {"type": "string"},
                    "caption_desc": {"type": "string"},
                    "visual": {"type": "string"},
                    "duration_sec": {"type": "number"},
                    "asset_refs": {"type": "array", "maxItems": 0, "items": {"type": "string"}},
                },
            },
        },
        "music_mood": {"type": "string"},
        "selected_engine": {"type": "string", "enum": ["motion"]},
    },
}

DIRECTOR_INSTRUCTIONS = """You are Oasis Video Director, a sharp creative director for short vertical product launch reels.
Create one cinematic-but-renderable production plan from the user's brief.

Rules:
- Make a 15-30 second, 9:16, 30 FPS reel.
- Create exactly five beats in this exact order: hook, value, product, proof, CTA. Use those exact intent values only.
- Every beat must have concise, original on-screen copy that is easy to read in 2-5 seconds.
- Use only kinetic_hook, kinetic_point, and outro_cta scene types.
- Beat durations must add up exactly to duration_sec.
- Use a safe #RRGGBB accent color. If no website is given, use https://example.com as cta_url.
- Set asset_refs to an empty array for every beat. Only the local asset mapper may attach real screenshot paths.
- Do not invent customer metrics, testimonials, partnerships, or named companies.
- Return only the requested JSON object.
"""


def generate_ai_plan(brief: str, duration_sec: int = 20) -> VideoPlan:
    """Use the Responses API to produce a structured, renderer-ready plan."""
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for --ai. Add it to your local .env file.")

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=os.environ.get("OASIS_MODEL", DEFAULT_MODEL),
        reasoning={"effort": "low"},
        instructions=DIRECTOR_INSTRUCTIONS,
        input=f"Target duration: {duration_sec} seconds.\n\nProduct brief:\n{brief}",
        text={
            "format": {
                "type": "json_schema",
                "name": "video_plan",
                "strict": True,
                "schema": PLAN_SCHEMA,
            }
        },
    )
    return plan_from_payload(json.loads(response.output_text))


def plan_from_payload(payload: dict[str, Any]) -> VideoPlan:
    """Convert a validated API payload into the shared Python plan schema."""
    brand = payload["brand"]
    beats = [
        Beat(
            id=beat["id"],
            intent=beat["intent"],
            scene_type=beat["scene_type"],
            spoken=beat["spoken"],
            caption_heading=beat["caption_heading"],
            caption_desc=beat["caption_desc"],
            visual=beat["visual"],
            duration_sec=beat["duration_sec"],
            asset_refs=beat["asset_refs"],
        )
        for beat in payload["beats"]
    ]
    return VideoPlan(
        title=payload["title"],
        format=payload["format"],
        duration_sec=payload["duration_sec"],
        fps=payload["fps"],
        brand=Brand(
            name=brand["name"],
            accent=brand["accent"],
            cta_url=brand["cta_url"],
        ),
        beats=beats,
        music_mood=payload["music_mood"],
        selected_engine=payload["selected_engine"],
    )