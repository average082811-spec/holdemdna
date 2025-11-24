import json
from pathlib import Path

import pytest

from holdemdna.cli import main


def write_profile(path: Path) -> None:
    payload = {
        "name": "Tmp Player",
        "mindset_notes": [],
        "baseline_vpip": 0.2,
        "baseline_pfr": 0.18,
        "risk_tolerance": 0.5,
        "sessions": [
            {
                "hours_played": 2.0,
                "hands_played": 150,
                "net_profit": 50,
                "vpip": 0.21,
                "pfr": 0.19,
                "three_bet": 0.05,
                "aggression_factor": 2.0,
                "tilt_events": 0,
                "showdown_win_rate": 0.55,
            }
        ],
    }
    path.write_text(json.dumps(payload))


def test_main_outputs_json(tmp_path, capsys):
    profile_path = tmp_path / "profile.json"
    write_profile(profile_path)

    exit_code = main([str(profile_path), "--json"])

    captured = capsys.readouterr()
    assert exit_code == 0
    data = json.loads(captured.out)
    assert set(data.keys()) >= {"strategy_score", "psychology_score", "mental_score", "composite"}


def test_main_errors_on_missing_profile(tmp_path):
    missing = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError):
        main([str(missing), "--json"])


def test_main_errors_on_invalid_json(tmp_path):
    invalid = tmp_path / "broken.json"
    invalid.write_text("not-json")

    with pytest.raises(ValueError):
        main([str(invalid), "--json"])
