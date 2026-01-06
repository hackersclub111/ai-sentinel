from ai_sentinel.ingestion import ingest_logs
from ai_sentinel.storage import store_records, query_logs
from ai_sentinel.feature_engineering import extract_features
from ai_sentinel.anomaly_detection import detect_anomalies
from ai_sentinel.explanation import generate_report
from ai_sentinel.alerting import send_alert







DEMO_MODE = True


DEMO_THRESHOLD = 0.4   # More sensitive → visible behavior
PROD_THRESHOLD = 0.8   # Conservative → low false positives


PROD_WINDOW_SIZE = 50
DEMO_WINDOW_SIZE = None  # None = score only the new batch


def run_prediction_pipeline(new_logs: list[dict], demo_mode: bool = DEMO_MODE) -> dict:
    

    # 1. Ingest + validate
    ingest_result = ingest_logs(new_logs)
    clean_logs = ingest_result.get("clean_logs", [])

    if not clean_logs:
        print("No valid logs received after ingestion.")
        return {"status": "no_valid_logs"}

    # 2. Persist logs

    store_records(clean_logs)


    # 3. Select scoring window

    if demo_mode:
        # Demo: focus only on latest batch so anomalies are visible
        recent_df = query_logs().tail(len(clean_logs))
        threshold = DEMO_THRESHOLD
        mode_label = "DEMO"
    else:
        # Production: broader context for stability
        recent_df = query_logs().tail(PROD_WINDOW_SIZE)
        threshold = PROD_THRESHOLD
        mode_label = "PRODUCTION"

    if recent_df.empty:
        print("No data available for scoring.")
        return {"status": "no_data_for_scoring"}


    # 4. Feature extraction

    features = extract_features(recent_df)


    # 5. Anomaly detection

    scored = detect_anomalies(features)

    # Explicit thresholding (DO NOT rely blindly on model defaults)
    scored["is_anomaly_effective"] = scored["anomaly_score"] >= threshold

    anomalies = scored[scored["is_anomaly_effective"]]


    # 6. Explain + alert

    if not anomalies.empty:
        anomalies_for_explain = anomalies[
            ["latency_z", "token_trend", "anomaly_score"]
        ].reset_index(drop=True)

        reports = generate_report(anomalies_for_explain)

        send_alert(reports)

        print(
            f"[{mode_label}] ALERT GENERATED | "
            f"anomalies={len(anomalies)} | threshold={threshold}"
        )

        return {
            "status": "alert_generated",
            "mode": mode_label,
            "anomalies": len(anomalies),
            "threshold": threshold,
        }


    # 7. Healthy run

    print(
        f"[{mode_label}] Pipeline healthy | "
        f"no anomalies | threshold={threshold}"
    )

    return {
        "status": "healthy",
        "mode": mode_label,
        "anomalies": 0,
        "threshold": threshold,
    }





if __name__ == "__main__":

    print("\n Running DEMO anomaly scenario")
    demo_logs = [
        {"timestamp": "2026-01-05T12:00:00", "latency_ms": 1500, "tokens_used": 4000},
        {"timestamp": "2026-01-05T12:01:00", "latency_ms": 160, "tokens_used": 1050},
    ]
    run_prediction_pipeline(demo_logs, demo_mode=True)

    print("\n Running PRODUCTION-like scenario")
    prod_logs = [
        {"timestamp": "2026-01-05T12:02:00", "latency_ms": 150, "tokens_used": 1000},
        {"timestamp": "2026-01-05T12:03:00", "latency_ms": 155, "tokens_used": 1020},
    ]
    run_prediction_pipeline(prod_logs, demo_mode=False)
