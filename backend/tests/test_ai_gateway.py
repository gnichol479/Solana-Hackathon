import json

import httpx
import pytest

from app.config import Settings
from app.models.schemas import AIStatus, IndicatorSource
from app.services import ai_gateway
from app.services.ai_gateway import (
    FallbackPaymentTextAnalyzer,
    OpenAIPaymentTextAnalyzer,
    OllamaPaymentTextAnalyzer,
    build_payment_text_analyzer,
)


@pytest.mark.asyncio
async def test_fallback_returns_quoted_explainable_warning() -> None:
    result = await FallbackPaymentTextAnalyzer().analyze(
        "URGENT: Send the wire immediately. Do not contact accounting."
    )

    assert result.performed is False
    assert result.status == AIStatus.FALLBACK
    assert {item.code for item in result.indicators} == {
        "urgent_payment_pressure",
        "discourages_independent_verification",
    }
    assert all(item.evidence for item in result.indicators)
    assert all(item.next_action for item in result.indicators)


def _mock_provider(monkeypatch, payload: dict, captured: dict | None = None) -> None:
    class MockResponse:
        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"choices": [{"message": {"content": json.dumps(payload)}}]}

    class MockClient:
        def __init__(self, **kwargs) -> None:
            self.options = kwargs

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args) -> None:
            return None

        async def post(self, url: str, **kwargs) -> MockResponse:
            if captured is not None:
                captured.update({"url": url, **kwargs})
            return MockResponse()

    monkeypatch.setattr(ai_gateway.httpx, "AsyncClient", MockClient)


@pytest.mark.asyncio
async def test_provider_keeps_only_findings_with_verbatim_evidence(monkeypatch) -> None:
    captured: dict = {}
    _mock_provider(
        monkeypatch,
        {
            "indicators": [
                {
                    "code": "unusual_payment_destination",
                    "category": "payment_instructions",
                    "severity": "warning",
                    "message": "The destination is not described clearly.",
                    "evidence": "purchase funds",
                    "next_action": "Confirm the payment details independently.",
                },
                {
                    "code": "unsupported_claim",
                    "category": "recipient",
                    "severity": "warning",
                    "message": "This evidence was not in the request.",
                    "evidence": "recipient owns account 555",
                    "next_action": "Verify through a known contact.",
                },
            ]
        },
        captured,
    )

    text = "Please send the purchase funds to our requested destination."
    result = await OpenAIPaymentTextAnalyzer("test-key", "test-model", 2).analyze(text)

    assert result.performed is True
    assert result.status == AIStatus.OK
    assert len(result.indicators) == 1
    assert result.indicators[0].source == IndicatorSource.AI
    assert result.indicators[0].evidence == "purchase funds"
    assert result.indicators[0].next_action
    assert captured["url"] == "https://api.openai.com/v1/chat/completions"
    assert captured["json"]["messages"][1] == {"role": "user", "content": text}
    assert "tools" not in captured["json"]


@pytest.mark.asyncio
async def test_provider_drops_finding_without_exact_quote(monkeypatch) -> None:
    _mock_provider(
        monkeypatch,
        {
            "indicators": [
                {
                    "code": "invented_evidence",
                    "category": "recipient",
                    "severity": "warning",
                    "message": "The recipient is suspicious.",
                    "evidence": "phrase absent from request",
                    "next_action": "Verify independently.",
                }
            ]
        },
    )

    result = await OpenAIPaymentTextAnalyzer("test-key", "test-model", 2).analyze(
        "Please review this payment request."
    )

    assert result.status == AIStatus.OK
    assert result.indicators == []
    assert "does not verify the recipient" in result.explanation


@pytest.mark.asyncio
async def test_provider_failure_keeps_local_checks(monkeypatch) -> None:
    class FailingClient:
        def __init__(self, **kwargs) -> None:
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args) -> None:
            return None

        async def post(self, *args, **kwargs):
            raise httpx.ReadTimeout("provider timed out")

    monkeypatch.setattr(ai_gateway.httpx, "AsyncClient", FailingClient)

    result = await OpenAIPaymentTextAnalyzer("test-key", "test-model", 2).analyze(
        "URGENT: Send the payment immediately."
    )

    assert result.performed is False
    assert result.status == AIStatus.UNAVAILABLE
    assert result.indicators[0].code == "urgent_payment_pressure"
    assert result.indicators[0].source == IndicatorSource.DETERMINISTIC


def test_analyzer_uses_local_fallback_without_api_key() -> None:
    analyzer = build_payment_text_analyzer(Settings(openai_api_key=None))

    assert isinstance(analyzer, FallbackPaymentTextAnalyzer)


def test_analyzer_selects_ollama_without_a_hosted_key() -> None:
    analyzer = build_payment_text_analyzer(Settings(ai_provider="ollama"))

    assert isinstance(analyzer, OllamaPaymentTextAnalyzer)
