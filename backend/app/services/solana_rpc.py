from typing import Any

import httpx

from app.config import Settings


class SolanaRpcError(RuntimeError):
    """Raised when a Solana JSON-RPC request cannot produce a usable result."""


class SolanaRpcClient:
    def __init__(self, settings: Settings, rpc_url: str | None = None) -> None:
        self._settings = settings
        self._rpc_url = rpc_url or settings.solana_rpc_url

    async def call(self, method: str, params: list[Any]) -> Any:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params,
        }

        try:
            async with httpx.AsyncClient(timeout=self._settings.solana_timeout_seconds) as client:
                response = await client.post(self._rpc_url, json=payload)
                response.raise_for_status()
                body = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise SolanaRpcError(f"Solana RPC request failed for {method}") from exc

        if not isinstance(body, dict):
            raise SolanaRpcError(f"Solana RPC returned an invalid response for {method}")

        if body.get("error") is not None:
            raise SolanaRpcError(f"Solana RPC returned an error for {method}")

        return body.get("result")

    async def get_account_info(self, address: str) -> dict[str, Any]:
        result = await self.call(
            "getAccountInfo",
            [
                address,
                {
                    "encoding": "base64",
                    "commitment": self._settings.solana_commitment,
                },
            ],
        )
        if not isinstance(result, dict):
            raise SolanaRpcError("Solana getAccountInfo returned an invalid result")
        return result

    async def get_balance(self, address: str) -> dict[str, Any]:
        result = await self.call(
            "getBalance",
            [address, {"commitment": self._settings.solana_commitment}],
        )
        if not isinstance(result, dict):
            raise SolanaRpcError("Solana getBalance returned an invalid result")
        return result

    async def get_signatures_for_address(self, address: str, limit: int) -> list[dict[str, Any]]:
        result = await self.call(
            "getSignaturesForAddress",
            [
                address,
                {
                    "limit": limit,
                    "commitment": self._settings.solana_commitment,
                },
            ],
        )
        if not isinstance(result, list):
            raise SolanaRpcError("Solana getSignaturesForAddress returned an invalid result")
        return [item for item in result if isinstance(item, dict)]
