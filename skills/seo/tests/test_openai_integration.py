import json
from types import SimpleNamespace

from openai_integration import make_openai_judge, make_openai_metadata_generator


class FakeResponses:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(output_text=json.dumps(self.payload, ensure_ascii=False))


class FakeClient:
    def __init__(self, payload):
        self.responses = FakeResponses(payload)


def test_openai_judge_returns_json_payload():
    client = FakeClient({
        "status": "PASS",
        "issues": [],
        "evidence": [],
        "reason": "aligned",
    })

    judge = make_openai_judge(model="gpt-test", client=client)
    result = judge("semantic_metadata", {"frontmatter": {"title": "검색"}})

    assert result["status"] == "PASS"
    assert client.responses.calls[0]["model"] == "gpt-test"


def test_openai_judge_maps_provider_error_to_failure():
    class BrokenResponses:
        def create(self, **kwargs):
            raise RuntimeError("boom")

    judge = make_openai_judge(client=SimpleNamespace(responses=BrokenResponses()))
    result = judge("semantic_metadata", {})

    assert result["status"] == "FAIL"
    assert result["issues"][0].startswith("openai_unavailable:")


def test_openai_metadata_generator_returns_candidate():
    client = FakeClient({
        "candidate": {
            "title": "생성 제목",
            "description": "생성 설명",
            "categories": ["Translation"],
            "image": "",
        },
        "warnings": [],
    })

    generator = make_openai_metadata_generator(model="gpt-test", client=client)
    result = generator({"frontmatter": {}, "content": {"first_heading": "원문 제목"}})

    assert result["candidate"]["title"] == "생성 제목"
    assert result["warnings"] == []
