This project is for Solana Hackathon 2026

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
python -m uvicorn app.main:app --reload --port 8000
```

The backend is read-only on Solana for the MVP. It does not require Phantom,
wallet connection, private keys, or seed phrases. See [backend/README.md](backend/README.md)
and [docs/api-contract.md](docs/api-contract.md) for the API contract.
