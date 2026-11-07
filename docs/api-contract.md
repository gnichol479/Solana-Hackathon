# Shared API Contract

The website and Chrome extension use the same backend contract. Request bodies
must not contain private keys, seed phrases, or unnecessary personal data.

## `GET /api/health`

Returns backend availability and the configured Solana network.

## `POST /api/analyze`

Request:

```json
{
  "text": "Send 100 USDC to this Solana wallet immediately.",
  "source": "extension"
}
```

`source` must be `website`, `extension`, or `api`.

Response shape:

```json
{
  "analysis_id": "analysis-...",
  "created_at": "2026-11-06T00:00:00Z",
  "source": "extension",
  "payment_type": "solana",
  "risk_level": "needs_verification",
  "summary": "The available information contains a warning sign or cannot be independently verified.",
  "indicators": [
    {
      "code": "missing_solana_recipient",
      "category": "recipient",
      "severity": "warning",
      "source": "deterministic",
      "message": "The request appears to involve Solana, but no wallet address was identified.",
      "evidence": null
    }
  ],
  "payment_details": {
    "amount": 100,
    "currency": "USDC",
    "recipient": null,
    "payment_url": null
  },
  "ai_analysis": {
    "performed": false,
    "status": "fallback",
    "indicators": [],
    "explanation": "The AI module is not configured yet; only basic deterministic message checks ran."
  },
  "solana_analysis": {
    "performed": false,
    "network": "devnet",
    "wallet_address": null,
    "address_valid": null,
    "account_exists": null,
    "sol_balance": null,
    "recent_transaction_count": null,
    "recent_transactions": [],
    "rpc_status": "missing_address",
    "message": "A Solana payment was detected, but no wallet address was provided."
  }
}
```

`risk_level` is one of:

- `suspicious`
- `needs_verification`
- `no_major_warnings_detected`

`no_major_warnings_detected` does not mean the payment is safe. It means the
available checks did not find a major warning.

## `GET /api/solana/wallet/{address}`

Returns read-only evidence for a syntactically valid Solana public key. The
response reports the configured network, account existence, SOL balance,
recent signatures, and explorer links. It does not identify the real-world
owner of an address.
