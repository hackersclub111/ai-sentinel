import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../../data/sentinel.db")

def store_records(records: list[dict]) -> dict:
    """
    Responsibility: Persist sanitized log records to SQLite.
    Input: List of dicts with keys: timestamp, latency_ms, tokens_used, error_type (optional)
    Output: {"tx_id": str} - simple success ID (row count)
    MUST NOT: Transform data or call other modules.
    """
    if not records:
        raise ValueError("Empty records list")

    # Step-by-step: Create DF, connect, append
    df = pd.DataFrame(records)
    
    # Ensure required columns (contract implies validation upstream)
    required = ["timestamp", "latency_ms", "tokens_used"]
    if not all(col in df.columns for col in required):
        raise ValueError("Missing required columns")

    conn = sqlite3.connect(DB_PATH)
    # Create table if first run
    conn.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            latency_ms INTEGER NOT NULL,
            tokens_used INTEGER NOT NULL,
            error_type TEXT
        )
    """)
    df.to_sql("logs", conn, if_exists="append", index=False)
    row_count = len(df)
    conn.commit()
    conn.close()
    
    return {"tx_id": f"success_{row_count}_rows"}

def query_logs(filter: dict = None) -> pd.DataFrame:
    """
    Input: filter dict e.g. {"from_date": "2026-01-01", "to_date": "2026-01-05"}
    Output: DataFrame of logs
    """
    if filter is None:
        filter = {}
        
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT id, timestamp, latency_ms, tokens_used, error_type FROM logs"
    conditions = []
    params = []
    
    if "from_date" in filter:
        conditions.append("timestamp >= ?")
        params.append(filter["from_date"])
    if "to_date" in filter:
        conditions.append("timestamp <= ?")
        params.append(filter["to_date"])
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY timestamp"
    
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df
