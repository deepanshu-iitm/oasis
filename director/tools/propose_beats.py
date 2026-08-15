"""Propose a concise, renderer-ready five-beat video arc."""

from __future__ import annotations

from director.schema import Beat


BEAT_ARC = ("hook", "value", "product", "proof", "cta")


def propose_beats(parsed: dict[str, object], duration_sec: int = 20) -> list[Beat]:
    """Create a hook-to-CTA sequence whose beat durations total the target."""
    if duration_sec < len(BEAT_ARC):
        raise ValueError("Duration must allow at least one second per beat.")

    product = str(parsed["product"])
    title = str(parsed["title"])
    cta = str(parsed["cta"])
    base_duration, remainder = divmod(duration_sec, len(BEAT_ARC))
    durations = [base_duration + (index < remainder) for index in range(len(BEAT_ARC))]

    content = (
        ("kinetic_hook", title, "A better way starts here.", "Bold kinetic type with a fast push-in."),
        ("kinetic_point", "Built for confidence", product, "Clear value statement with flowing text."),
        ("kinetic_point", "Meet the product", product, "Product-focused kinetic type."),
        ("kinetic_point", "Why it matters", "Simple, trustworthy, and made to move you forward.", "Proof-point type sequence."),
        ("outro_cta", cta, title, "Clean logo-style lockup and confident finish."),
    )

    return [
        Beat(
            id=f"b{index:02d}",
            intent=intent,
            scene_type=scene_type,
            spoken=f"{heading}. {description}",
            caption_heading=heading,
            caption_desc=description,
            visual=visual,
            duration_sec=duration,
        )
        for index, (intent, duration, (scene_type, heading, description, visual)) in enumerate(
            zip(BEAT_ARC, durations, content), start=1
        )
    ]