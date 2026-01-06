from ai_sentinel.ingestion import ingest_logs

def test_ingest_valid():
    logs = [{"timestamp": "2026-01-05T12:00:00", "latency_ms": 150, "tokens_used": 1000}]
    result = ingest_logs(logs)
    assert result["ingested"] == 1
    assert len(result["rejected"]) == 0

def test_ingest_invalid():
    logs = [{"timestamp": "bad", "latency_ms": 150, "tokens_used": 1000}]
    result = ingest_logs(logs)
    assert result["ingested"] == 0
    assert len(result["rejected"]) == 1
