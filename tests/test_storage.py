import pytest
from ai_sentinel.storage import store_records, query_logs

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/sentinel.db")
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)  # Clean for test

def test_store_and_query():
    records = [
        {"timestamp": "2026-01-05T12:00:00", "latency_ms": 150, "tokens_used": 1000},
        {"timestamp": "2026-01-05T12:01:00", "latency_ms": 160, "tokens_used": 1050}
    ]
    result = store_records(records)
    assert "success_2_rows" in result["tx_id"]
    
    df = query_logs()
    assert len(df) == 2
    assert df.iloc[0]["latency_ms"] == 150
    
    # Filter test
    filtered = query_logs({"from_date": "2026-01-05T12:01:00"})
    assert len(filtered) == 1
