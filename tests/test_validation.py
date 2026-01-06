def test_validation_metrics_exist_and_range():
    import pandas as pd
    from ai_sentinel.validation import validate_model

    test_df = pd.DataFrame({
        "timestamp": [
            "2026-01-05T12:00:00",
            "2026-01-05T12:01:00",
            "2026-01-05T12:02:00",
            "2026-01-05T12:03:00",
            "2026-01-05T12:04:00",
            "2026-01-05T12:05:00"
        ],
        "latency_ms": [150, 155, 160, 2000, 2100, 2200],
        "tokens_used": [1000, 1010, 1020, 5000, 5100, 5200]
    })

    labels = [False, False, False, True, True, True]

    metrics = validate_model(test_df, labels)

    # Contract checks (NOT accuracy assumptions)
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1" in metrics

    for k in ["precision", "recall", "f1"]:
        assert 0.0 <= metrics[k] <= 1.0
