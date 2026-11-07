import json

import httpx
import pytest

from app.config import Settings
from app.models.schemas import AIStatus, IndicatorSource
from app.services import ai_gateway
from app.services.ai_gateway import (
    FallbackPaymentTextAnalyzer,
    GeminiPaymentTextAnalyzer,
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
            return {
                "candidates": [
                    {"content": {"parts": [{"text": json.dumps(payload)}]}}
                ]
            }

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
async def test_gemini_keeps_only_findings_with_verbatim_evidence(monkeypatch) -> None:
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
    result = await GeminiPaymentTextAnalyzer(
        "test-key", "test-model", "https://generativelanguage.test/v1beta", 2
    ).analyze(text)

    assert result.performed is True
    assert result.status == AIStatus.OK
    assert len(result.indicators) == 1
    assert result.indicators[0].source == IndicatorSource.AI
    assert result.indicators[0].evidence == "purchase funds"
    assert result.indicators[0].next_action
    assert captured["url"] == (
        "https://generativelanguage.test/v1beta/models/test-model:generateContent"
    )
    assert captured["headers"]["x-goog-api-key"] == "test-key"
    assert captured["json"]["contents"][0]["parts"][0]["text"] == text
    assert captured["json"]["generationConfig"]["responseMimeType"] == "application/json"
    assert captured["json"]["generationConfig"]["responseSchema"]["required"] == [
        "indicators"
    ]


@pytest.mark.asyncio
async def test_gemini_drops_finding_without_exact_quote(monkeypatch) -> None:
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

    result = await GeminiPaymentTextAnalyzer(
        "test-key", "test-model", "https://generativelanguage.test/v1beta", 2
    ).analyze("Please review this payment request.")

    assert result.status == AIStatus.OK
    assert result.indicators == []
    assert "does not verify the recipient" in result.explanation


@pytest.mark.asyncio
async def test_gemini_failure_keeps_local_checks(monkeypatch) -> None:
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

    result = await GeminiPaymentTextAnalyzer(
        "test-key", "test-model", "https://generativelanguage.test/v1beta", 2
    ).analyze("URGENT: Send the payment immediately.")

    assert result.performed is False
    assert result.status == AIStatus.UNAVAILABLE
    assert result.indicators[0].code == "urgent_payment_pressure"
    assert result.indicators[0].source == IndicatorSource.DETERMINISTIC


def test_analyzer_uses_local_fallback_without_api_key() -> None:
    analyzer = build_payment_text_analyzer(Settings(gemini_api_key=None))

    assert isinstance(analyzer, FallbackPaymentTextAnalyzer)


def test_analyzer_selects_gemini_with_a_hosted_key() -> None:
    analyzer = build_payment_text_analyzer(
        Settings(ai_provider="gemini", gemini_api_key="test-key")
    )

    assert isinstance(analyzer, GeminiPaymentTextAnalyzer)
