"""Command-line entry point for Codex Video Director."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m director",
        description="Turn a product brief into a short marketing video.",
    )
    parser.add_argument(
        "brief",
        nargs="?",
        help="Product brief to direct (implementation coming next).",
    )
    return parser


def main() -> None:
    parser = build_parser()
    parser.parse_args()


if __name__ == "__main__":
    main()