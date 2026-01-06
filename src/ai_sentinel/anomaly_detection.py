import pickle
import os
from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../data/model.pkl")

def train_model(features_df: pd.DataFrame):
    """Internal helper - train on assumed normal data"""
    if features_df.empty:
        raise ValueError("No features to train")
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(features_df)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

def detect_anomalies(features_df: pd.DataFrame, model_path: str = None) -> pd.DataFrame:
    """
    Input: Feature DataFrame
    Output: Original + anomaly_score (0-1 normalized), is_anomaly (True if score > 0.8)
    Logic: Load model (or raise if missing), predict
    """
    global MODEL_PATH
    if model_path:
        load_path = model_path
    else:
        load_path = MODEL_PATH
        
    if not os.path.exists(load_path):
        raise FileNotFoundError("Model not trained - run init script first")
        
    with open(load_path, "rb") as f:
        model = pickle.load(f)
    
    if features_df.empty:
        return features_df.assign(anomaly_score=0.0, is_anomaly=False)
    
    # decision_function: higher = more normal, negative = anomaly
    raw_scores = model.decision_function(features_df)
    # Normalize to 0-1 (higher = more anomalous)
    anomaly_scores = 1 - (raw_scores - raw_scores.min()) / (raw_scores.max() - raw_scores.min() + 1e-6)
    anomaly_scores = np.clip(anomaly_scores, 0, 1)
    
    result_df = features_df.copy()
    result_df["anomaly_score"] = anomaly_scores
    result_df["is_anomaly"] = anomaly_scores > 0.8  # Tunable threshold
    
    return result_df
