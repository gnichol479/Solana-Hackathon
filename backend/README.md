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

The backend can use local Ollama, OpenAI, or only deterministic checks. Each
model finding must include an exact quote from the submitted text; unsupported
quotes are discarded. If the selected provider is unavailable, local checks
still run and the response reports that AI analysis was unavailable.

For the no-cost local setup, install Ollama for Windows, run `ollama pull
llama3.2`, and use these backend settings:

```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3.2
```

The Ollama API stays on the local machine. The backend never sends the request
to a hosted AI provider when `AI_PROVIDER=ollama`.

The OpenAI option remains available by setting `AI_PROVIDER=openai`,
`OPENAI_API_KEY`, and `OPENAI_MODEL`. Never commit `.env` files or API keys.

After setting the key, restart the backend and check `GET /api/health` for
`"ai_configured": true`. A successful analysis then reports
`ai_analysis.performed: true` and `ai_analysis.status: "ok"`; a missing or
failed provider remains visible as a local fallback instead of blocking the
analysis.
