"""Data models describing poker players and sessions."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class SessionSnapshot:
    """Single poker session statistics."""

    hours_played: float
    hands_played: int
    net_profit: float
    vpip: float  # voluntarily put money in pot percentage
    pfr: float  # pre-flop raise percentage
    three_bet: float  # three-bet percentage
    aggression_factor: float
    tilt_events: int
    showdown_win_rate: float

    def volume_score(self) -> float:
        """Return a normalized volume score based on hours and hands."""
        hands_score = min(self.hands_played / 500, 1)
        hours_score = min(self.hours_played / 8, 1)
        return round((hands_score * 0.6 + hours_score * 0.4) * 100, 2)


@dataclass
class PlayerProfile:
    """Aggregated player data across multiple sessions."""

    name: str
    mindset_notes: List[str]
    baseline_vpip: float
    baseline_pfr: float
    risk_tolerance: float  # 0-1 scale
    sessions: List[SessionSnapshot] = field(default_factory=list)

    def recent_sessions(self, n: int = 3) -> List[SessionSnapshot]:
        """Return the N most recent sessions (default 3)."""
        return self.sessions[-n:]


@dataclass
class SessionReport:
    """Summary of strategy, psychology, and mental metrics."""

    strategy_score: float
    psychology_score: float
    mental_score: float
    recommendations: List[str]

    @property
    def composite(self) -> float:
        """Overall composite index."""
        return round(
            self.strategy_score * 0.4
            + self.psychology_score * 0.3
            + self.mental_score * 0.3,
            2,
        )


__all__ = ["SessionSnapshot", "PlayerProfile", "SessionReport"]
