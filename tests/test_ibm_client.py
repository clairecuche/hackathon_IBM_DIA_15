import json
from backend import ibm_client


def test_extract_metrics_from_prediction():
    # sample IBM WML-like prediction response with some of the required fields
    sample = {
        "predictions": [
            {
                "fields": [
                    "prompt_token_length",
                    "response_token_length",
                    "prompt_speed_tps",
                    "model_name_encoded",
                ],
                "values": [[12, 48, 0.5, "my_model_v1"]],
            }
        ]
    }

    metrics = ibm_client.extract_metrics(sample, prompt="hello world example")

    assert metrics["prompt_token_length"] == 12
    assert metrics["response_token_length"] == 48
    assert abs(metrics["prompt_speed_tps"] - 0.5) < 1e-9
    assert metrics["model_name_encoded"] == "my_model_v1"


def test_extract_metrics_with_missing_fields():
    sample = {"predictions": []}
    metrics = ibm_client.extract_metrics(sample, prompt="one two three four")
    # fallback estimated tokens (4 words)
    assert metrics["prompt_token_length"] == 4
