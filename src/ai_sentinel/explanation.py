import pandas as pd

def generate_report(anomalies_df: pd.DataFrame) -> list[dict]:
    """
    Input: DataFrame with is_anomaly=True rows + feature columns
    Output: List of report dicts (deterministic templates)
    MUST NOT: Use real AI (hallucination risk)
    """
    if anomalies_df.empty or "is_anomaly" not in anomalies_df.columns:
        return []
        
    reports = []
    for _, row in anomalies_df[anomalies_df["is_anomaly"]].iterrows():
        causes = []
        recs = []
        
        if row["latency_z"] > 2:
            causes.append("latency_spike")
            recs.append("scale compute resources or optimize prompts")
        if abs(row["token_trend"]) > 0.5:
            causes.append("context_drift_or_overflow")
            recs.append("implement chunking or increase token limit")
            
        cause_str = ", ".join(causes) or "unknown_anomaly"
        rec_str = "; ".join(recs) or "investigate logs manually"
        
        reports.append({
            "cause": cause_str,
            "confidence": round(row["anomaly_score"], 2),
            "recommendation": rec_str
        })
    
    return reports
