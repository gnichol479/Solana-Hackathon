import pytest

from app.config import Settings
from app.models.schemas import SolanaRpcStatus
from app.services.solana_analysis import SolanaAnalysisService
from app.services.solana_rpc import SolanaRpcError


SYSTEM_PROGRAM = "11111111111111111111111111111111"


class FakeRpc:
    async def get_account_info(self, address: str) -> dict:
        return {"context": {"slot": 1}, "value": {"owner": "11111111111111111111111111111111"}}

    async def get_balance(self, address: str) -> dict:
        return {"context": {"slot": 1}, "value": 2_500_000_000}

    async def get_signatures_for_address(self, address: str, limit: int) -> list[dict]:
        return [
            {
                "signature": "demo-signature",
                "slot": 42,
                "blockTime": 1_700_000_000,
                "err": None,
            }
        ]


class UnavailableRpc:
    async def get_account_info(self, address: str) -> dict:
        raise SolanaRpcError("offline")


@pytest.mark.asyncio
async def test_returns_read_only_wallet_evidence() -> None:
    result = await SolanaAnalysisService(Settings(), rpc_client=FakeRpc()).analyze(SYSTEM_PROGRAM)

    assert result.performed is True
    assert result.rpc_status == SolanaRpcStatus.OK
    assert result.address_valid is True
    assert result.account_exists is True
    assert result.sol_balance == 2.5
    assert result.recent_transaction_count == 1
    assert result.recent_transactions[0].signature == "demo-signature"


@pytest.mark.asyncio
async def test_does_not_call_rpc_for_missing_address() -> None:
    result = await SolanaAnalysisService(Settings(), rpc_client=UnavailableRpc()).analyze(None)

    assert result.performed is False
    assert result.rpc_status == SolanaRpcStatus.MISSING_ADDRESS


@pytest.mark.asyncio
async def test_reports_rpc_unavailability_without_inventing_data() -> None:
    result = await SolanaAnalysisService(Settings(), rpc_client=UnavailableRpc()).analyze(SYSTEM_PROGRAM)

    assert result.performed is True
    assert result.rpc_status == SolanaRpcStatus.UNAVAILABLE
    assert result.sol_balance is None
    assert result.recent_transactions == []
