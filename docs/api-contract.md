# Shared API Contract

The website and Chrome extension use the same backend contract. Request bodies
must not contain private keys, seed phrases, or unnecessary personal data.

For local development, the extension calls `http://127.0.0.1:8001` and sends
`Origin: chrome-extension://<extension-id>`. The development backend accepts
valid Chrome extension origins; production deployments should allow only the
specific published extension ID.

## `GET /api/health`

Returns backend availability, the configured Solana network, the selected AI
provider, and whether that provider is configured. `ai_configured` reports
configuration only; the analysis response reports whether a provider call
actually completed.

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
      "evidence": null,
      "next_action": "Confirm the wallet address with the recipient through a trusted channel."
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
    "explanation": "Local text checks ran. Configure an AI provider key to enable optional AI-assisted findings."
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

Indicators may include evidence with an exact quote from the request and a next_action recommendation. AI findings without a verbatim quote are omitted.

The backend runs deterministic checks without a provider key. Optional AI-assisted analysis uses OPENAI_API_KEY, OPENAI_MODEL, and AI_TIMEOUT_SECONDS from the backend environment. Provider errors leave local checks available and set the AI status to unavailable.

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
