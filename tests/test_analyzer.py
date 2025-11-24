from holdemdna.analyzer import analyze_player
from holdemdna.models import PlayerProfile, SessionSnapshot


def sample_profile() -> PlayerProfile:
    sessions = [
        SessionSnapshot(
            hours_played=5,
            hands_played=400,
            net_profit=150,
            vpip=0.26,
            pfr=0.21,
            three_bet=0.09,
            aggression_factor=2.5,
            tilt_events=1,
            showdown_win_rate=0.55,
        ),
        SessionSnapshot(
            hours_played=6,
            hands_played=480,
            net_profit=-80,
            vpip=0.25,
            pfr=0.2,
            three_bet=0.08,
            aggression_factor=2.2,
            tilt_events=2,
            showdown_win_rate=0.52,
        ),
    ]
    return PlayerProfile(
        name="Tester",
        mindset_notes=["Solid warmup"],
        baseline_vpip=0.25,
        baseline_pfr=0.21,
        risk_tolerance=0.7,
        sessions=sessions,
    )


def test_analyze_player_scores_are_in_range():
    profile = sample_profile()
    report = analyze_player(profile)
    for metric in (report.strategy_score, report.psychology_score, report.mental_score):
        assert 0 <= metric <= 100
    assert report.recommendations
    assert isinstance(report.composite, float)
