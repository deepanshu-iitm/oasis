"""Perform lightweight quality checks on a renderer-facing video plan."""

from __future__ import annotations

from math import isclose

from director.schema import VideoPlan


ALLOWED_SCENE_TYPES = {"kinetic_hook", "kinetic_point", "outro_cta", "phone_single"}
REQUIRED_INTENTS = {"hook", "value", "product", "proof", "cta"}


def critique_plan(plan: VideoPlan) -> dict[str, object]:
    """Return actionable issues and fixes for a proposed video plan."""
    issues: list[str] = []
    fixes: list[str] = []
    total_duration = sum(beat.duration_sec for beat in plan.beats)
    intents = {beat.intent for beat in plan.beats}
    unsupported_scenes = sorted(
        {beat.scene_type for beat in plan.beats if beat.scene_type not in ALLOWED_SCENE_TYPES}
    )

    if not plan.beats:
        issues.append("The plan has no beats.")
        fixes.append("Add a hook, value, product, proof, and CTA beat.")
    if not isclose(total_duration, plan.duration_sec):
        issues.append(
            f"Beat duration totals {total_duration:g}s, not the requested {plan.duration_sec:g}s."
        )
        fixes.append("Adjust beat durations so they total the target duration.")
    if missing_intents := REQUIRED_INTENTS - intents:
        issues.append(f"Missing required beat intents: {', '.join(sorted(missing_intents))}.")
        fixes.append("Include each part of the hook-to-CTA arc.")
    if unsupported_scenes:
        issues.append(f"Unsupported scene types: {', '.join(unsupported_scenes)}.")
        fixes.append("Use only the scene types supported by the v1 renderer.")
    if not plan.brand.cta_url:
        issues.append("The brand CTA URL is empty.")
        fixes.append("Add a CTA URL before publishing the video.")

    return {"ok": not issues, "issues": issues, "fixes": fixes}