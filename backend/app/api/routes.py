from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Query

from app.config import SolanaNetwork, get_settings
from app.models.schemas import AnalysisRequest, AnalysisResponse, SolanaAnalysis
from app.services.ai_gateway import FallbackPaymentTextAnalyzer
from app.services.payment_detection import detect_payment_request
from app.services.risk import compose_risk
from app.services.solana_analysis import SolanaAnalysisService, build_not_run_result


router = APIRouter(prefix="/api")
settings = get_settings()
solana_service = SolanaAnalysisService(settings)
ai_analyzer = FallbackPaymentTextAnalyzer()


@router.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "ok",
        "environment": settings.app_env,
        "solana_network": settings.solana_network,
    }


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    detection = detect_payment_request(request.text)
    ai_analysis = await ai_analyzer.analyze(request.text)

    if detection.payment_type.value == "solana":
        solana_analysis = await solana_service.analyze(detection.wallet_address)
    else:
        solana_analysis = build_not_run_result(settings)

    risk_level, summary, indicators = compose_risk(
        detection.payment_type,
        detection.payment_details,
        ai_analysis,
        solana_analysis,
    )

    return AnalysisResponse(
        analysis_id=f"analysis-{uuid4().hex}",
        created_at=datetime.now(timezone.utc),
        source=request.source,
        payment_type=detection.payment_type,
        risk_level=risk_level,
        summary=summary,
        indicators=indicators,
        payment_details=detection.payment_details,
        ai_analysis=ai_analysis,
        solana_analysis=solana_analysis,
    )


@router.get("/solana/wallet/{address}", response_model=SolanaAnalysis)
async def analyze_solana_wallet(
    address: str,
    network: SolanaNetwork | None = Query(default=None),
) -> SolanaAnalysis:
    return await solana_service.analyze(address, network=network)
