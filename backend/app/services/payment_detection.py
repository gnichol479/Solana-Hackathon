import re
from dataclasses import dataclass

from app.models.schemas import PaymentDetails, PaymentType


_BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_BASE58_INDEX = {character: index for index, character in enumerate(_BASE58_ALPHABET)}
_SOLANA_TOKEN_PATTERN = re.compile(
    r"(?<![1-9A-HJ-NP-Za-km-z])[1-9A-HJ-NP-Za-km-z]{32,44}(?![1-9A-HJ-NP-Za-km-z])"
)
_URL_PATTERN = re.compile(r"https?://[^\s<>\"]+", re.IGNORECASE)
_SOLANA_HINT_PATTERN = re.compile(r"\b(solana|sol|usdc|spl\s+token|phantom\s+wallet)\b", re.IGNORECASE)
_TRADITIONAL_HINT_PATTERN = re.compile(
    r"\b(bank|wire|ach|paypal|venmo|zelle|invoice|credit\s+card|debit\s+card|account\s+number)\b",
    re.IGNORECASE,
)
_AMOUNT_CURRENCY_PATTERN = re.compile(
    r"(?P<amount>\d+(?:,\d{3})*(?:\.\d+)?)\s*(?P<currency>USDC|SOL|USD)\b",
    re.IGNORECASE,
)
_DOLLAR_AMOUNT_PATTERN = re.compile(r"\$\s*(?P<amount>\d+(?:,\d{3})*(?:\.\d+)?)\b")


@dataclass(frozen=True)
class PaymentDetection:
    payment_type: PaymentType
    payment_details: PaymentDetails
    wallet_address: str | None


def _decode_base58(value: str) -> bytes | None:
    if not value or any(character not in _BASE58_INDEX for character in value):
        return None

    number = 0
    for character in value:
        number = number * 58 + _BASE58_INDEX[character]

    raw = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    leading_zeroes = len(value) - len(value.lstrip("1"))
    return b"\x00" * leading_zeroes + raw


def is_valid_solana_address(value: str) -> bool:
    """Validate the syntactic shape of a Solana public key.

    This confirms only that the value is a valid base58-encoded 32-byte public
    key. It does not prove that the address belongs to a person or is safe.
    """

    decoded = _decode_base58(value)
    return decoded is not None and len(decoded) == 32


def extract_solana_address(text: str) -> str | None:
    for candidate in _SOLANA_TOKEN_PATTERN.findall(text):
        if is_valid_solana_address(candidate):
            return candidate
    return None


def _extract_amount_and_currency(text: str) -> tuple[float | None, str | None]:
    match = _AMOUNT_CURRENCY_PATTERN.search(text)
    if match:
        return float(match.group("amount").replace(",", "")), match.group("currency").upper()

    match = _DOLLAR_AMOUNT_PATTERN.search(text)
    if match:
        return float(match.group("amount").replace(",", "")), "USD"

    return None, None


def detect_payment_request(text: str) -> PaymentDetection:
    wallet_address = extract_solana_address(text)
    amount, currency = _extract_amount_and_currency(text)
    payment_url_match = _URL_PATTERN.search(text)

    if wallet_address or _SOLANA_HINT_PATTERN.search(text):
        payment_type = PaymentType.SOLANA
    elif _TRADITIONAL_HINT_PATTERN.search(text):
        payment_type = PaymentType.TRADITIONAL
    else:
        payment_type = PaymentType.UNKNOWN

    return PaymentDetection(
        payment_type=payment_type,
        wallet_address=wallet_address,
        payment_details=PaymentDetails(
            amount=amount,
            currency=currency,
            recipient=wallet_address,
            payment_url=payment_url_match.group(0) if payment_url_match else None,
        ),
    )
