from app.config import Settings
from app.models.schemas import AIAnalysis, AIStatus, PaymentDetails, PaymentType, RiskLevel, SolanaRpcStatus
from app.services.risk import compose_risk
from app.services.solana_analysis import build_not_run_result


def test_missing_solana_recipient_requires_verification() -> None:
    settings = Settings()
    risk_level, summary, indicators = compose_risk(
        PaymentType.SOLANA,
        PaymentDetails(currency="USDC"),
        AIAnalysis(performed=False, status=AIStatus.FALLBACK),
        build_not_run_result(settings, status=SolanaRpcStatus.MISSING_ADDRESS),
    )

    assert risk_level == RiskLevel.NEEDS_VERIFICATION
    assert "verif" in summary.lower()
    assert any(indicator.code == "missing_solana_recipient" for indicator in indicators)


def test_two_independent_warning_signals_are_suspicious() -> None:
    settings = Settings()
    ai = AIAnalysis(
        performed=False,
        status=AIStatus.FALLBACK,
        indicators=[
            {
                "code": "urgent_payment_pressure",
                "category": "message",
                "severity": "warning",
                "source": "deterministic",
                "message": "Urgency",
            },
            {
                "code": "discourages_independent_verification",
                "category": "message",
                "severity": "warning",
                "source": "deterministic",
                "message": "No verification",
            },
        ],
    )

    risk_level, _, _ = compose_risk(
        PaymentType.TRADITIONAL,
        PaymentDetails(amount=500, currency="USD"),
        ai,
        build_not_run_result(settings),
    )

    assert risk_level == RiskLevel.SUSPICIOUS
