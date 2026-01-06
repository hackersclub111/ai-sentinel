def send_alert(report: list[dict], channel: str = "api") -> dict:
    """
    Local MVP: Print or return (in Zerve use webhook/email)
    """
    if not report:
        return {"status": "no_alert_needed"}
        
    if channel == "api":
        # In production/Zerve: return for HTTP response
        return {"status": "sent_via_api", "report": report}
    else:
        # Debug print
        print("ALERT:", report)
        return {"status": "printed_locally"}
