"""Command-line entry point for Codex Video Director."""

from __future__ import annotations

import argparse

from director.agent import run_director


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m director",
        description="Turn a product brief into a short marketing video plan.",
    )
    parser.add_argument("brief", help="Product brief to direct.")
    parser.add_argument(
        "--out",
        default="out/demo",
        help="Directory for plan.json, storyboard.md, and final.mp4 (default: out/demo).",
    )
    parser.add_argument(
        "--duration-sec",
        type=int,
        default=20,
        help="Target video duration in seconds (default: 20).",
    )
    parser.add_argument(
        "--screenshot",
        action="append",
        default=[],
        help="Optional screenshot path; repeat for up to two screenshots.",
    )
    parser.add_argument(
        "--no-render",
        action="store_true",
        help="Create plan.json and storyboard.md without rendering final.mp4.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = run_director(
        args.brief,
        args.out,
        duration_sec=args.duration_sec,
        screenshot_paths=args.screenshot,
        render=not args.no_render,
        on_step=lambda step: print(f"[director] {step}"),
    )
    print(f"[director] Wrote {result.plan_path}")
    print(f"[director] Wrote {result.storyboard_path}")
    if result.final_video_path:
        print(f"[director] Wrote {result.final_video_path}")
    if not result.critique["ok"]:
        print(f"[director] Plan needs review: {result.critique['issues']}")


if __name__ == "__main__":
    main()