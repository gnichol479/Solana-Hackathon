from datetime import datetime, timezone
from uuid import uuid4

from io import BytesIO

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from pypdf import PdfReader

from app.config import SolanaNetwork, get_settings
from app.models.schemas import AnalysisRequest, AnalysisResponse, SolanaAnalysis
from app.services.ai_gateway import build_payment_text_analyzer
from app.services.payment_detection import detect_payment_request
from app.services.risk import compose_risk
from app.services.solana_analysis import SolanaAnalysisService, build_not_run_result


router = APIRouter(prefix="/api")
settings = get_settings()
solana_service = SolanaAnalysisService(settings)
ai_analyzer = build_payment_text_analyzer(settings)
MAX_DOCUMENT_BYTES = 10 * 1024 * 1024
SUPPORTED_DOCUMENT_TYPES = {"application/pdf", "image/png", "image/jpeg"}


@router.get("/health")
async def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "environment": settings.app_env,
        "solana_network": settings.solana_network,
        "ai_provider": settings.ai_provider,
        "ai_configured": settings.ai_provider == "ollama"
        or bool((settings.openai_api_key or "").strip()),
    }


async def _analyze_text(request: AnalysisRequest, extracted_text: str | None = None) -> AnalysisResponse:
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
        extracted_text=extracted_text,
    )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    return await _analyze_text(request)


@router.post("/analyze-document", response_model=AnalysisResponse)
async def analyze_document(
    file: UploadFile = File(...),
    text: str | None = Form(default=None),
) -> AnalysisResponse:
    """Analyze a user-selected document without retaining its bytes.

    Images are OCR'd in the browser and send their reviewed text here. PDFs
    can be text-extracted server-side when the browser has no OCR text to send.
    """
    if file.content_type not in SUPPORTED_DOCUMENT_TYPES:
        raise HTTPException(status_code=415, detail="Choose a PDF, PNG, or JPG document.")

    raw = await file.read(MAX_DOCUMENT_BYTES + 1)
    if len(raw) > MAX_DOCUMENT_BYTES:
        raise HTTPException(status_code=413, detail="Choose a document under 10 MB.")

    extracted = (text or "").strip()
    if file.content_type == "application/pdf" and not extracted:
        try:
            reader = PdfReader(BytesIO(raw), strict=False)
            extracted = "\n".join(page.extract_text() or "" for page in reader.pages).strip()
        except Exception as exc:
            raise HTTPException(status_code=422, detail="The PDF text could not be extracted.") from exc

    if not extracted:
        raise HTTPException(
            status_code=422,
            detail="No readable text was supplied. Use Screenshot & QR to OCR an image, then review it before analysis.",
        )

    validated = AnalysisRequest(text=extracted, source="website")
    return await _analyze_text(validated, extracted_text=extracted)


@router.get("/solana/wallet/{address}", response_model=SolanaAnalysis)
async def analyze_solana_wallet(
    address: str,
    network: SolanaNetwork | None = Query(default=None),
) -> SolanaAnalysis:
    return await solana_service.analyze(address, network=network)
