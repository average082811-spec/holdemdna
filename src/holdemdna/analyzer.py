"""Core analysis routines for HoldemDNA."""
from __future__ import annotations

from dataclasses import asdict
from statistics import mean
from typing import Dict, List

from .models import PlayerProfile, SessionReport, SessionSnapshot


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, round(value, 2)))


def _variance_penalty(values: List[float]) -> float:
    if not values:
        return 0
    avg = mean(values)
    return min(sum(abs(v - avg) for v in values) / (len(values) * 5), 1) * 25


def _trend_score(values: List[float]) -> float:
    if len(values) < 2:
        return 50
    diffs = [b - a for a, b in zip(values, values[1:])]
    trend = sum(diffs) / len(diffs)
    return 50 + trend * 10


def _psychology_score(profile: PlayerProfile) -> float:
    tilt_events = [session.tilt_events for session in profile.sessions]
    if not tilt_events:
        return 75
    stability = 100 - min(mean(tilt_events) * 8, 80)
    notes_penalty = 5 * sum("tilt" in note.lower() for note in profile.mindset_notes)
    return _clamp(stability - notes_penalty)


def _strategy_score(profile: PlayerProfile) -> float:
    if not profile.sessions:
        return 50
    recent = profile.recent_sessions(5)
    vpip_dev = mean(abs(s.vpip - profile.baseline_vpip) for s in recent)
    pfr_dev = mean(abs(s.pfr - profile.baseline_pfr) for s in recent)
    aggression = mean(s.aggression_factor for s in recent)
    showdown = mean(s.showdown_win_rate for s in recent)
    vpip_component = max(0, 30 - vpip_dev * 300)
    pfr_component = max(0, 30 - pfr_dev * 300)
    aggression_component = min(aggression / 3 * 20, 20)
    showdown_component = min(showdown * 20, 20)
    trend_component = _trend_score([s.net_profit for s in recent]) * 0.2
    return _clamp(
        vpip_component
        + pfr_component
        + aggression_component
        + showdown_component
        + trend_component
    )


def _mental_score(profile: PlayerProfile) -> float:
    risk_factor = profile.risk_tolerance * 100
    volume_scores = [s.volume_score() for s in profile.sessions]
    volume = mean(volume_scores) if volume_scores else 40
    variance_penalty = _variance_penalty([s.net_profit for s in profile.sessions])
    return _clamp(0.6 * volume + 0.4 * (100 - variance_penalty) - (100 - risk_factor) * 0.2)


def analyze_player(profile: PlayerProfile) -> SessionReport:
    """Generate a session report for the provided player profile."""
    strategy = _strategy_score(profile)
    psychology = _psychology_score(profile)
    mental = _mental_score(profile)
    recommendations = _generate_recommendations(profile, strategy, psychology, mental)
    return SessionReport(
        strategy_score=strategy,
        psychology_score=psychology,
        mental_score=mental,
        recommendations=recommendations,
    )


def _generate_recommendations(
    profile: PlayerProfile, strategy: float, psychology: float, mental: float
) -> List[str]:
    recs: List[str] = []
    if strategy < 60:
        recs.append(
            "Review baseline VPIP/PFR combos and tighten opening ranges for early position."
        )
    if psychology < 60:
        recs.append("Schedule mindset warmups; document tilt triggers in detail after each session.")
    if mental < 60:
        recs.append(
            "Balance volume with recovery. Use breathing resets when variance spikes mid-session."
        )
    if not recs:
        recs.append("Great form! Maintain the current preparation and review cadence.")
    recent = profile.recent_sessions(1)
    if recent:
        recs.append(
            f"Latest session summary: {recent[0].hands_played} hands, {recent[0].net_profit:+.1f}bb."
        )
    return recs


def serialize_report(report: SessionReport) -> Dict[str, float | List[str]]:
    """Serialize report to primitive types for JSON export."""
    payload: Dict[str, float | List[str]] = asdict(report)
    payload["composite"] = report.composite
    return payload


__all__ = ["analyze_player", "serialize_report"]
