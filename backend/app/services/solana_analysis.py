from datetime import datetime, timezone
from typing import Any

from app.config import Settings
from app.models.schemas import SolanaAnalysis, SolanaRpcStatus, SolanaTransaction
from app.services.payment_detection import is_valid_solana_address
from app.services.solana_rpc import SolanaRpcClient, SolanaRpcError


def _explorer_suffix(network: str) -> str:
    return "" if network == "mainnet-beta" else f"?cluster={network}"


def build_not_run_result(
    settings: Settings,
    status: SolanaRpcStatus = SolanaRpcStatus.NOT_RUN,
    message: str | None = None,
) -> SolanaAnalysis:
    return SolanaAnalysis(
        performed=False,
        network=settings.solana_network,
        rpc_status=status,
        message=message,
    )


class SolanaAnalysisService:
    def __init__(self, settings: Settings, rpc_client: SolanaRpcClient | Any | None = None) -> None:
        self._settings = settings
        self._rpc = rpc_client or SolanaRpcClient(settings)

    async def analyze(self, address: str | None) -> SolanaAnalysis:
        if not address:
            return build_not_run_result(
                self._settings,
                status=SolanaRpcStatus.MISSING_ADDRESS,
                message="A Solana payment was detected, but no wallet address was provided.",
            )

        if not is_valid_solana_address(address):
            return SolanaAnalysis(
                performed=False,
                network=self._settings.solana_network,
                wallet_address=address,
                address_valid=False,
                rpc_status=SolanaRpcStatus.INVALID_ADDRESS,
                message="The supplied value is not a syntactically valid Solana address.",
            )

        try:
            account_info = await self._rpc.get_account_info(address)
            balance_info = await self._rpc.get_balance(address)
            signatures = await self._rpc.get_signatures_for_address(
                address,
                self._settings.solana_signature_limit,
            )
        except SolanaRpcError:
            return SolanaAnalysis(
                performed=True,
                network=self._settings.solana_network,
                wallet_address=address,
                address_valid=True,
                rpc_status=SolanaRpcStatus.UNAVAILABLE,
                message="Solana public data could not be retrieved from the configured RPC endpoint.",
            )

        account_exists = account_info.get("value") is not None
        balance_value = balance_info.get("value")
        lamports = balance_value if isinstance(balance_value, int) else None
        sol_balance = lamports / 1_000_000_000 if lamports is not None else None
        suffix = _explorer_suffix(self._settings.solana_network)

        transactions: list[SolanaTransaction] = []
        for item in signatures:
            signature = item.get("signature")
            if not isinstance(signature, str):
                continue

            block_time = None
            if isinstance(item.get("blockTime"), int):
                block_time = datetime.fromtimestamp(item["blockTime"], tz=timezone.utc)

            slot = item.get("slot") if isinstance(item.get("slot"), int) else None
            status = "failed" if item.get("err") is not None else "success"
            transactions.append(
                SolanaTransaction(
                    signature=signature,
                    slot=slot,
                    block_time=block_time,
                    status=status,
                    explorer_url=f"https://explorer.solana.com/tx/{signature}{suffix}",
                )
            )

        account_message = (
            "The address is syntactically valid and returned account data on the selected network."
            if account_exists
            else "The address is syntactically valid, but no account data was returned on the selected network."
        )

        return SolanaAnalysis(
            performed=True,
            network=self._settings.solana_network,
            wallet_address=address,
            address_valid=True,
            account_exists=account_exists,
            sol_balance=sol_balance,
            recent_transaction_count=len(transactions),
            recent_transactions=transactions,
            rpc_status=SolanaRpcStatus.OK,
            message=account_message,
        )
