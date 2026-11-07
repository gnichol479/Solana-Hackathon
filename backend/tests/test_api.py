import httpx
import pytest
import pytest_asyncio

from app.main import app


@pytest_asyncio.fixture
async def client() -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client


@pytest.mark.asyncio
async def test_health_endpoint(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_analyze_returns_consistent_traditional_response(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/api/analyze",
        json={
            "text": "URGENT: pay this invoice immediately by bank wire. Do not contact the vendor.",
            "source": "website",
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["payment_type"] == "traditional"
    assert body["risk_level"] == "suspicious"
    assert body["solana_analysis"]["rpc_status"] == "not_run"
    assert body["indicators"]


@pytest.mark.asyncio
async def test_document_upload_accepts_browser_ocr_text(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/api/analyze-document",
        data={"text": "URGENT: send 100 USDC on Solana immediately."},
        files={"file": ("request.png", b"not-used-after-browser-ocr", "image/png")},
    )

    body = response.json()
    assert response.status_code == 200
    assert body["payment_type"] == "solana"
    assert body["extracted_text"].startswith("URGENT")
    assert body["indicators"]


@pytest.mark.asyncio
async def test_document_upload_rejects_unsupported_type(client: httpx.AsyncClient) -> None:
    response = await client.post(
        "/api/analyze-document",
        files={"file": ("request.svg", b"<svg />", "image/svg+xml")},
    )

    assert response.status_code == 415
