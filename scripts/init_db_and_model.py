import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from ai_sentinel.storage import store_records, query_logs
from ai_sentinel.feature_engineering import extract_features
from ai_sentinel.anomaly_detection import train_model
import os

# Generate 200 synthetic NORMAL logs
logs = []
start_time = datetime(2026, 1, 1)
for i in range(150):
    ts = (start_time + timedelta(minutes=i)).isoformat()
    latency = int(np.random.normal(150, 20))  # Normal ~150ms
    tokens = 1000 + i * 5 + int(np.random.normal(0, 30))  # Gradual increase
    logs.append({
        "timestamp": ts,
        "latency_ms": max(50, latency),  # Prevent negative
        "tokens_used": max(100, tokens),
        "error_type": "none"
    })

# Store + train
store_records(logs)
df = query_logs()
features = extract_features(df)
train_model(features)
print("Initial DB and model created with 200 normal logs")
# Add 50 anomalies
anomaly_logs = []
for i in range(50):
    ts = (start_time + timedelta(minutes=150 + i)).isoformat()
    latency = int(np.random.normal(1500, 200))  # High latency
    tokens = 4000 + i * 10 + int(np.random.normal(0, 100))
    anomaly_logs.append({
        "timestamp": ts,
        "latency_ms": max(1000, latency),
        "tokens_used": max(3000, tokens),
        "error_type": "hallucination"
    })
store_records(anomaly_logs)
print("Added 50 anomalies for validation")
