import json

from pricing_sim.vllm_benchmark import parse_completion_stream


def test_parse_completion_stream_extracts_text_and_usage():
    lines = [
        "data: "
        + json.dumps(
            {
                "choices": [{"text": "A"}],
                "usage": None,
            }
        ),
        "data: "
        + json.dumps(
            {
                "choices": [{"text": "B"}],
                "usage": {
                    "prompt_tokens": 7,
                    "completion_tokens": 20,
                    "total_tokens": 27,
                },
            }
        ),
        "data: [DONE]",
    ]

    result = parse_completion_stream(lines)

    assert result["stream_chunks"] == 2
    assert result["output_characters"] == 2
    assert result["prompt_tokens"] == 7
    assert result["generated_tokens"] == 20
