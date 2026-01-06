import pandas as pd
import numpy as np

def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Responsibility: Transform raw logs → ML features.
    Input: DataFrame with raw columns + timestamp
    Output: DataFrame with feature columns only (for model)
    Logic step-by-step:
    1. Sort by timestamp
    2. Compute z-score latency, token trend (pct_change)
    3. Handle NaN (first row trend = 0)
    """
    if df.empty:
        raise ValueError("Empty DataFrame")
        
    df = df.copy()
    df = df.sort_values("timestamp")
    
    # Basic features
    df["latency_z"] = (df["latency_ms"] - df["latency_ms"].mean()) / (df["latency_ms"].std() + 1e-6)  # Avoid div0
    df["token_trend"] = df["tokens_used"].pct_change().fillna(0)
    
    # Return only features (contract: add columns, but we return minimal for model)
    features_df = df[["latency_z", "token_trend"]].copy()
    
    # Replace any remaining inf/nan
    features_df = features_df.replace([np.inf, -np.inf], 0).fillna(0)
    
    return features_df
