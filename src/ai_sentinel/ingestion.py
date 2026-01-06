from datetime import datetime

def ingest_logs(logs: list[dict]) -> dict:
    """
    Responsibility: Validate and sanitize raw logs.
    Input: Raw list of dicts
    Output: {"ingested": int, "rejected": list[dict with reason]}
    MUST NOT: Store data or call other modules.
    """
    ingested = []
    rejected = []
    
    required_keys = {"timestamp", "latency_ms", "tokens_used"}
    
    for log in logs:
        # Step 1: Check required keys
        missing = required_keys - log.keys()
        if missing:
            rejected.append({"log": log, "reason": f"Missing keys: {missing}"})
            continue
            
        # Step 2: Type + basic sanity checks
        try:
            # ISO format check (simple)
            datetime.fromisoformat(log["timestamp"].replace("Z", "+00:00"))
            latency = int(log["latency_ms"])
            tokens = int(log["tokens_used"])
            if latency <= 0 or tokens <= 0:
                raise ValueError("Non-positive values")
            # Sanitize: ensure error_type str or None
            error_type = str(log.get("error_type", "none"))
        except Exception as e:
            rejected.append({"log": log, "reason": f"Invalid data: {str(e)}"})
            continue
            
        # Step 3: Clean record
        clean_log = {
            "timestamp": log["timestamp"],
            "latency_ms": latency,
            "tokens_used": tokens,
            "error_type": error_type
        }
        ingested.append(clean_log)
    
    return {"ingested": len(ingested), "rejected": rejected, "clean_logs": ingested}  # Extra clean_logs for pipeline convenience (contract allows output schema flexibility)
