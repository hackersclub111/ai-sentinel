from ai_sentinel.alerting import send_alert

def test_alert_api():
    report = [{"cause": "test", "confidence": 0.9, "recommendation": "fix"}]
    result = send_alert(report, "api")
    assert result["status"] == "sent_via_api"

def test_no_report():
    result = send_alert([])
    assert result["status"] == "no_alert_needed"
