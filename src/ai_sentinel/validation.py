import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score
from ai_sentinel.anomaly_detection import detect_anomalies
from ai_sentinel.feature_engineering import extract_features

def validate_model(test_df: pd.DataFrame, labels: list[bool]) -> dict:
    """
    Input: Raw test logs DF + true_anomaly labels (same order)
    Output: Metrics dict
    Logic: Extract features → detect → compute metrics vs ground truth
    """
    if len(test_df) != len(labels):
        raise ValueError("Mismatch lengths")
        
    features = extract_features(test_df)
    scored = detect_anomalies(features)
    predicted = scored["is_anomaly"].tolist()
    
    return {
        "precision": round(precision_score(labels, predicted), 3),
        "recall": round(recall_score(labels, predicted), 3),
        "f1": round(f1_score(labels, predicted), 3)
    }

# Example synthetic validation in README
