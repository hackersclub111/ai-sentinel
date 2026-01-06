def test_detect_anomalies_output_schema():
    import pandas as pd
    from ai_sentinel.feature_engineering import extract_features
    from ai_sentinel.anomaly_detection import detect_anomalies

    df = pd.DataFrame({
        "timestamp": [
            "2026-01-05T12:00:00",
            "2026-01-05T12:01:00",
            "2026-01-05T12:02:00"
        ],
        "latency_ms": [150, 155, 160],
        "tokens_used": [1000, 1010, 1020]
    })

    features = extract_features(df)
    scored = detect_anomalies(features)

    # Assertions that ALWAYS hold
    assert "anomaly_score" in scored.columns
    assert "is_anomaly" in scored.columns
    assert len(scored) == len(features)

    # Scores must be valid probabilities
    assert scored["anomaly_score"].between(0, 1).all()
