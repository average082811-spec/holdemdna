"""Command line interface for HoldemDNA analysis."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analyzer import analyze_player, serialize_report
from .models import PlayerProfile, SessionSnapshot


def _load_profile(path: Path) -> PlayerProfile:
    data = json.loads(path.read_text())
    sessions = [SessionSnapshot(**session) for session in data.pop("sessions", [])]
    return PlayerProfile(**data, sessions=sessions)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="HoldemDNA Purple Lab analyzer")
    parser.add_argument("profile", type=Path, help="Path to a JSON profile file")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Return JSON instead of a formatted summary",
    )
    args = parser.parse_args(argv)

    profile = _load_profile(args.profile)
    report = analyze_player(profile)

    if args.json:
        payload = serialize_report(report)
        print(json.dumps(payload, indent=2))
    else:
        _print_report(profile.name, report)
    return 0


def _print_report(name: str, report) -> None:
    print(f"HoldemDNA Report :: {name}")
    print("-" * 40)
    print(f"Strategy Score : {report.strategy_score:.1f}")
    print(f"Psychology Score: {report.psychology_score:.1f}")
    print(f"Mental Score   : {report.mental_score:.1f}")
    print(f"Composite Index: {report.composite:.1f}")
    print("\nRecommendations:")
    for idx, rec in enumerate(report.recommendations, 1):
        print(f"  {idx}. {rec}")


if __name__ == "__main__":
    raise SystemExit(main())
