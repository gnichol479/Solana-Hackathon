from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


SolanaNetwork = Literal["devnet", "testnet", "mainnet-beta"]
AIProvider = Literal["local", "openai", "ollama"]


class Settings(BaseSettings):
    """Runtime configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: Literal["development", "test", "production"] = "development"
    ai_provider: AIProvider = "local"
    openai_api_key: str | None = Field(default=None, repr=False)
    openai_model: str = "gpt-4.1-mini"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "llama3.2"
    ai_timeout_seconds: float = Field(default=25.0, gt=0, le=60)
    solana_network: SolanaNetwork = "devnet"
    solana_rpc_url: str = "https://api.devnet.solana.com"
    solana_commitment: Literal["processed", "confirmed", "finalized"] = "finalized"
    solana_signature_limit: int = Field(default=10, ge=1, le=100)
    solana_timeout_seconds: float = Field(default=8.0, gt=0, le=60)
    max_analysis_length: int = Field(default=20_000, ge=1_000, le=100_000)
    allowed_cors_origins: str = "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173"
    allowed_cors_origin_regex: str | None = None

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_cors_origins.split(",") if origin.strip()]

    @property
    def cors_origin_regex(self) -> str | None:
        if self.allowed_cors_origin_regex:
            return self.allowed_cors_origin_regex
        if self.app_env == "development":
            return r"^chrome-extension://[a-p]{32}$"
        return None

    def rpc_url_for_network(self, network: SolanaNetwork) -> str:
        if network == self.solana_network:
            return self.solana_rpc_url
        return {
            "devnet": "https://api.devnet.solana.com",
            "testnet": "https://api.testnet.solana.com",
            "mainnet-beta": "https://api.mainnet.solana.com",
        }[network]


@lru_cache
def get_settings() -> Settings:
    return Settings()
