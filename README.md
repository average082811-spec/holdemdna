# HoldemDNA

HoldemDNA 퍼플 랩 – 심리 × 전략 × 멘탈 분석 MVP

## 소개
이 저장소는 포커 플레이어의 세션 데이터를 기반으로 전략(Strategy) · 심리(Psychology) · 멘탈(Mental) 지표를 정량화하는 간단한 Python 패키지입니다. JSON 형태의 플레이어 프로필을 입력하면 HoldemDNA 분석 엔진이 종합 점수와 개선 권장사항을 제공합니다.

## 빠른 시작
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
holdemdna samples/sample_profile.json
```

JSON 결과가 필요하면 `--json` 플래그를 사용하세요.

```bash
holdemdna samples/sample_profile.json --json
```

## JSON 프로필 구조
```json
{
  "name": "플레이어 이름",
  "mindset_notes": ["메모1", "메모2"],
  "baseline_vpip": 0.25,
  "baseline_pfr": 0.22,
  "risk_tolerance": 0.65,
  "sessions": [
    {
      "hours_played": 6.5,
      "hands_played": 450,
      "net_profit": 220,
      "vpip": 0.27,
      "pfr": 0.23,
      "three_bet": 0.08,
      "aggression_factor": 2.8,
      "tilt_events": 1,
      "showdown_win_rate": 0.54
    }
  ]
}
```

## 테스트
```bash
python -m pytest
```

## 라이선스
MIT
