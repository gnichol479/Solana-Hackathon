import re
from typing import Protocol

from app.models.schemas import AIAnalysis, AIStatus, Indicator, IndicatorSeverity, IndicatorSource


class PaymentTextAnalyzer(Protocol):
    async def analyze(self, text: str) -> AIAnalysis:
        ...


class FallbackPaymentTextAnalyzer:
    """Small deterministic fallback used until Person 2's AI module is wired in."""

    async def analyze(self, text: str) -> AIAnalysis:
        indicators: list[Indicator] = []

        if re.search(r"\b(urgent|immediately|asap|right now|final notice)\b", text, re.IGNORECASE):
            indicators.append(
                Indicator(
                    code="urgent_payment_pressure",
                    category="message",
                    severity=IndicatorSeverity.WARNING,
                    source=IndicatorSource.DETERMINISTIC,
                    message="The request applies pressure to make the payment immediately.",
                )
            )

        if re.search(
            r"(do not|don't|never)\s+(contact|call|tell)|keep\s+this\s+secret|confidential",
            text,
            re.IGNORECASE,
        ):
            indicators.append(
                Indicator(
                    code="discourages_independent_verification",
                    category="message",
                    severity=IndicatorSeverity.WARNING,
                    source=IndicatorSource.DETERMINISTIC,
                    message="The request discourages independent verification of the payment instructions.",
                )
            )

        if re.search(
            r"\b(new|changed|updated|different)\s+(bank|payment|account)|change(d)?\s+the\s+payment",
            text,
            re.IGNORECASE,
        ):
            indicators.append(
                Indicator(
                    code="payment_instruction_change",
                    category="payment_instructions",
                    severity=IndicatorSeverity.WARNING,
                    source=IndicatorSource.DETERMINISTIC,
                    message="The request refers to changed or updated payment instructions.",
                )
            )

        explanation = None
        if indicators:
            explanation = "The fallback checks found message patterns that deserve independent verification."
        else:
            explanation = "The AI module is not configured yet; only basic deterministic message checks ran."

        return AIAnalysis(
            performed=False,
            status=AIStatus.FALLBACK,
            indicators=indicators,
            explanation=explanation,
        )
