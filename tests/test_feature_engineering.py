import pandas as pd
from ai_sentinel.feature_engineering import extract_features

def test_features():
    data = {
        "timestamp": ["2026-01-05T12:00:00", "2026-01-05T12:01:00"],
        "latency_ms": [150, 250],
        "tokens_used": [1000, 2000]
    }
    df = pd.DataFrame(data)
    features = extract_features(df)
    assert features.shape == (2, 2)
    assert abs(features.iloc[0]["latency_z"] + 0.7071) < 0.01
  # mean ~200, std ~70
    assert features.iloc[1]["token_trend"] == 1.0
