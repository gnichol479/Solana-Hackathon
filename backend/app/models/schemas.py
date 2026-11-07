from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class AnalysisSource(str, Enum):
    WEBSITE = "website"
    EXTENSION = "extension"
    API = "api"


class PaymentType(str, Enum):
    TRADITIONAL = "traditional"
    SOLANA = "solana"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    SUSPICIOUS = "suspicious"
    NEEDS_VERIFICATION = "needs_verification"
    NO_MAJOR_WARNINGS_DETECTED = "no_major_warnings_detected"


class IndicatorSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class IndicatorSource(str, Enum):
    DETERMINISTIC = "deterministic"
    AI = "ai"
    SOLANA = "solana"


class AIStatus(str, Enum):
    NOT_RUN = "not_run"
    OK = "ok"
    UNAVAILABLE = "unavailable"
    FALLBACK = "fallback"


class SolanaRpcStatus(str, Enum):
    NOT_RUN = "not_run"
    MISSING_ADDRESS = "missing_address"
    INVALID_ADDRESS = "invalid_address"
    OK = "ok"
    UNAVAILABLE = "unavailable"


class AnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = Field(min_length=1, max_length=20_000)
    source: AnalysisSource = AnalysisSource.API

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("text must contain non-whitespace characters")
        return value


class PaymentDetails(BaseModel):
    amount: float | None = None
    currency: str | None = None
    recipient: str | None = None
    payment_url: str | None = None


class Indicator(BaseModel):
    code: str
    category: str
    severity: IndicatorSeverity
    source: IndicatorSource
    message: str
    evidence: str | None = None


class AIAnalysis(BaseModel):
    performed: bool
    status: AIStatus
    indicators: list[Indicator] = Field(default_factory=list)
    explanation: str | None = None


class SolanaTransaction(BaseModel):
    signature: str
    slot: int | None = None
    block_time: datetime | None = None
    status: str
    explorer_url: str


class LegacySolanaTransaction(BaseModel):
    """Compatibility fields used by the existing frontend wallet panel."""

    signature: str
    blockTime: int | None = None
    err: bool | None = None


class SolanaAnalysis(BaseModel):
    performed: bool
    network: str
    wallet_address: str | None = None
    address_valid: bool | None = None
    account_exists: bool | None = None
    sol_balance: float | None = None
    recent_transaction_count: int | None = None
    recent_transactions: list[SolanaTransaction] = Field(default_factory=list)
    rpc_status: SolanaRpcStatus
    message: str | None = None
    balance_sol: float | None = None
    checked_at: datetime | None = None
    transactions: list[LegacySolanaTransaction] = Field(default_factory=list)
    tokens: list[dict[str, object]] = Field(default_factory=list)
    transaction_count: int | None = None
    known_scam_reports: int | None = None


class AnalysisResponse(BaseModel):
    analysis_id: str
    created_at: datetime
    source: AnalysisSource
    payment_type: PaymentType
    risk_level: RiskLevel
    summary: str
    indicators: list[Indicator] = Field(default_factory=list)
    payment_details: PaymentDetails
    ai_analysis: AIAnalysis
    solana_analysis: SolanaAnalysis
