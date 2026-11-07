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
python -m uvicorn app.main:app --reload --port 8001
```

WSL and Phantom are not required for this read-only backend.

Open the interactive API documentation at `http://127.0.0.1:8001/docs`.

## Example request

```powershell
$body = @{ text = "Send 100 USDC to 11111111111111111111111111111111"; source = "website" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8001/api/analyze -ContentType 'application/json' -Body $body
```

The default network is Devnet. Set `SOLANA_NETWORK` and `SOLANA_RPC_URL` in a
local `.env` file for another configured network. Keep RPC credentials out of
Git.

## AI analysis

The backend uses Gemini for optional AI-assisted findings or only deterministic
checks when no Gemini key is configured. Each model finding must include an
exact quote from the submitted text; unsupported quotes are discarded. If the
provider is unavailable, local checks still run and the response reports that
AI analysis was unavailable.

Create a Gemini API key in Google AI Studio and keep it only in the backend
environment. Use these settings:

```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your-server-side-key
GEMINI_MODEL=gemini-3.5-flash-lite
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta
```

Never commit `.env` files or API keys. The frontend and browser extension call
the backend; they never receive the Gemini key.

After setting the key, restart the backend and check `GET /api/health` for
`"ai_configured": true`. A successful analysis then reports
`ai_analysis.performed: true` and `ai_analysis.status: "ok"`; a missing or
failed provider remains visible as a local fallback instead of blocking the
analysis.
