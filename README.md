This project is for Solana Hackathon 2026

## Website — Person 3

The React website is in `frontend/`. For the integrated local stack on Windows, double-click `start-all.cmd`; it starts the analysis/Solana backend on port 8001, the account service on port 8002, and the Vite website on port 5173. If you only need the static frontend, use `start-website.cmd`.

It includes a landing page, request analysis, screenshot OCR, QR decoding, payment extraction, recipient wallet comparison and a Solana evidence section. Merchant examples are fictional and clearly labeled. See [frontend setup and integration instructions](frontend/README.md) and [feature status](docs/feature-status.md).

The [account and evidence service](account-service/README.md) implements account security, passkeys/FaceID through WebAuthn, and protected reports alongside Person 1's analysis/Solana backend. Deployment still requires persistent hosting and matching frontend API origins.

Solana Setup Steps:
wsl --install
Inside VS Code
node --version
npm --version
https://phantom.com/?utm_source=chatgpt.com
Create a hackathon account in Phantom
Open the Phantom browser extension.
Click your profile avatar in the upper-left corner.
Select Manage Accounts (pencil icon).
Click + → Create New Account.
Name it Solana Hackathon and click Create. 

Then enable Devnet:
Go to Settings → Developer Settings.
Turn on Testnet Mode.
Select Solana Devnet. 

Phantom Help Center

Backend Quick Start:

```powershell
Set-Location backend
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload --port 8001
```

The backend is read-only on Solana for the MVP. It does not require Phantom,
wallet connection, private keys, or seed phrases. See [backend/README.md](backend/README.md)
and [docs/api-contract.md](docs/api-contract.md) for the API contract.
