import pandas as pd
from ai_sentinel.explanation import generate_report

def test_report():
    data = {"latency_z": [3.0], "token_trend": [0.6], "anomaly_score": [0.9], "is_anomaly": [True]}
    df = pd.DataFrame(data)
    reports = generate_report(df)
    assert len(reports) == 1
    assert "latency_spike" in reports[0]["cause"]
    assert "context_drift_or_overflow" in reports[0]["cause"]
