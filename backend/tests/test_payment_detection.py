from app.models.schemas import PaymentType
from app.services.payment_detection import detect_payment_request, is_valid_solana_address


SYSTEM_PROGRAM = "11111111111111111111111111111111"


def test_detects_solana_wallet_and_payment_details() -> None:
    result = detect_payment_request(f"Send 100 USDC to {SYSTEM_PROGRAM} immediately.")

    assert result.payment_type == PaymentType.SOLANA
    assert result.wallet_address == SYSTEM_PROGRAM
    assert result.payment_details.amount == 100
    assert result.payment_details.currency == "USDC"


def test_detects_traditional_payment_request() -> None:
    result = detect_payment_request("Please pay the invoice by bank wire to the updated account.")

    assert result.payment_type == PaymentType.TRADITIONAL
    assert result.wallet_address is None


def test_solana_keyword_without_wallet_still_identifies_payment_type() -> None:
    result = detect_payment_request("Send the requested USDC payment through Solana.")

    assert result.payment_type == PaymentType.SOLANA
    assert result.wallet_address is None


def test_solana_address_validation_is_syntactic_only() -> None:
    assert is_valid_solana_address(SYSTEM_PROGRAM)
    assert not is_valid_solana_address("not-a-solana-address")
