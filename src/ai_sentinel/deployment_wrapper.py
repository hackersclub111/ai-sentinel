def deploy_pipeline(config: dict) -> dict:
    print("Local placeholder - in Zerve use UI to deploy API/schedule")
    print("Config received:", config)
    return {"url": "local_only", "status": "simulated"}

def trigger_retrain() -> str:
    print("Retraining not implemented in MVP - use init script")
    return "simulated"
