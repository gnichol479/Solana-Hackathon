from app.models.schemas import (
    AIAnalysis,
    Indicator,
    IndicatorSeverity,
    IndicatorSource,
    PaymentDetails,
    PaymentType,
    RiskLevel,
    SolanaAnalysis,
    SolanaRpcStatus,
)


def _add_once(indicators: list[Indicator], indicator: Indicator) -> None:
    if not any(existing.code == indicator.code for existing in indicators):
        indicators.append(indicator)


def compose_risk(
    payment_type: PaymentType,
    payment_details: PaymentDetails,
    ai_analysis: AIAnalysis,
    solana_analysis: SolanaAnalysis,
) -> tuple[RiskLevel, str, list[Indicator]]:
    indicators = list(ai_analysis.indicators)

    if payment_type == PaymentType.SOLANA:
        if not payment_details.recipient:
            _add_once(
                indicators,
                Indicator(
                    code="missing_solana_recipient",
                    category="recipient",
                    severity=IndicatorSeverity.WARNING,
                    source=IndicatorSource.DETERMINISTIC,
                    message="The request appears to involve Solana, but no wallet address was identified.",
                ),
            )

        if solana_analysis.rpc_status == SolanaRpcStatus.INVALID_ADDRESS:
            _add_once(
                indicators,
                Indicator(
                    code="invalid_solana_address",
                    category="recipient",
                    severity=IndicatorSeverity.WARNING,
                    source=IndicatorSource.SOLANA,
                    message="The supplied value is not a syntactically valid Solana address.",
                ),
            )
        elif solana_analysis.rpc_status == SolanaRpcStatus.MISSING_ADDRESS:
            _add_once(
                indicators,
                Indicator(
                    code="missing_solana_recipient",
                    category="recipient",
                    severity=IndicatorSeverity.WARNING,
                    source=IndicatorSource.SOLANA,
                    message="Blockchain analysis could not run because the wallet address is missing.",
                ),
            )
        elif solana_analysis.rpc_status == SolanaRpcStatus.UNAVAILABLE:
            _add_once(
                indicators,
                Indicator(
                    code="blockchain_unavailable",
                    category="solana",
                    severity=IndicatorSeverity.WARNING,
                    source=IndicatorSource.SOLANA,
                    message="Solana data could not be retrieved, so the recipient could not be fully checked.",
                ),
            )
        elif solana_analysis.account_exists is False:
            _add_once(
                indicators,
                Indicator(
                    code="account_not_found_on_network",
                    category="solana",
                    severity=IndicatorSeverity.WARNING,
                    source=IndicatorSource.SOLANA,
                    message="No account data was returned for this address on the selected network.",
                ),
            )

    warning_count = sum(
        indicator.severity in {IndicatorSeverity.WARNING, IndicatorSeverity.CRITICAL}
        for indicator in indicators
    )
    has_critical = any(indicator.severity == IndicatorSeverity.CRITICAL for indicator in indicators)

    if has_critical or warning_count >= 2:
        risk_level = RiskLevel.SUSPICIOUS
        summary = "Several warning signs were detected. Independently verify the recipient before paying."
    elif warning_count == 1:
        risk_level = RiskLevel.NEEDS_VERIFICATION
        summary = "The available information contains a warning sign or cannot be independently verified."
    else:
        risk_level = RiskLevel.NO_MAJOR_WARNINGS_DETECTED
        summary = "No major warnings were detected by the available checks. This is not proof the payment is safe."

    return risk_level, summary, indicators
