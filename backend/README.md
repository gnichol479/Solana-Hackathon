# Backend API

This is the shared FastAPI backend for the payment scam detection project.

The initial implementation is read-only on Solana. It validates public-key
syntax and queries public RPC data; it never requests wallet credentials,
signs transactions, or sends funds.

## Local setup on Windows PowerShell

From the repository root:

```powershell
Set-Location backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload --port 8000
```

WSL and Phantom are not required for this read-only backend.

Open the interactive API documentation at `http://127.0.0.1:8000/docs`.

## Example request

```powershell
$body = @{ text = "Send 100 USDC to 11111111111111111111111111111111"; source = "website" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/analyze -ContentType 'application/json' -Body $body
```

The default network is Devnet. Set `SOLANA_NETWORK` and `SOLANA_RPC_URL` in a
local `.env` file for another configured network. Keep RPC credentials out of
Git.

## Current integration boundary

`app/services/ai_gateway.py` contains a deterministic fallback analyzer so the
backend works before the separate AI module is ready. Person 2's structured
analyzer can replace `FallbackPaymentTextAnalyzer` without changing the API
response contract.
