from ai_sentinel.deployment_wrapper import deploy_pipeline

def test_deploy():
    config = {"type": "api", "modules": ["all"]}
    result = deploy_pipeline(config)
    assert result["status"] == "simulated"
