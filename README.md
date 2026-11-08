# Bait — Check Before You Pay

Bait is an AI-assisted payment scam investigation tool for people who want a second look before sending money. It helps users understand warning signs in a payment request and, when the request contains a Solana wallet, review public blockchain evidence alongside the message.

## Why Bait exists

Scam attempts are frequent and increasingly arrive through ordinary messages, invoices, links, and payment requests. In a June 2026 [AP-NORC survey](https://apnorc.org/projects/fifty-eight-percent-of-adults-report-receiving-scam-attempts-daily/), 58% of U.S. adults said they receive suspected scam attempts daily and 92% said they encounter them at least monthly. The same survey found that 17% had been scammed into giving away money and 24% had been scammed into providing personal information.

Bait is designed to create a pause before payment. It is decision support, not a guarantee that a payment is safe.

## How it works

1. **Bring in the request.** Users can paste a message or invoice, upload an image or PDF, scan a QR code, or use the browser extension to analyze selected text.
2. **Extract useful details.** The frontend can use OCR and QR decoding to find payment amounts, currencies, URLs, Solana addresses, and other payment information.
3. **Analyze warning signs.** Local checks identify patterns such as urgency, threats, impersonation, changed payment instructions, suspicious links, and requests to bypass normal verification. When the team backend is connected, Gemini adds explainable findings that must quote the submitted text.
4. **Add Solana context.** For a Solana request, the backend validates the public address and performs read-only RPC lookups for the selected network. The report can show SOL balance, supported token balances, recent transaction signatures, timestamps, and links to Solana Explorer.
5. **Explain what remains unknown.** A valid or active wallet does not prove ownership, identity, or safety. Recipient comparison is intentionally conservative, and the demonstration registry is fictional and clearly labeled.

The website and Manifest V3 browser extension use the same analysis API. An optional account service provides password/PIN authentication, WebAuthn passkeys such as Face ID or Windows Hello, CSRF-protected sessions, and opt-in saved reports. No feature connects a wallet, requests a seed phrase or private key, signs a transaction, or sends funds.

## Architecture

```text
Website / Chrome extension
            │
            ▼
     FastAPI analysis API ──► Gemini (optional AI findings)
            │
            └───────────────► Solana public RPC / Explorer

     Account service ──► authentication, passkeys, saved reports
```

## Technology stack

- **Frontend:** React, Vite, JavaScript, HTML, CSS
- **Input processing:** Tesseract.js OCR, jsQR, QRCode, PDF parsing
- **Backend:** Python, FastAPI, Uvicorn, Pydantic, HTTPX
- **AI:** Google Gemini with structured, server-side responses
- **Blockchain:** Solana public RPC and Solana Explorer
- **Accounts:** SQLite, Argon2, WebAuthn/passkeys
- **Extension and hosting:** Chrome Manifest V3 and Vercel

## Run locally

On Windows, install the dependencies described in the service READMEs, then run:

```powershell
./start-all.cmd
```

This starts:

- Website: `http://localhost:5173`
- Analysis and Solana API: `http://127.0.0.1:8001`
- Account and reports API: `http://localhost:8002`

The backend defaults to Solana Devnet and remains read-only. To enable Gemini, put the server-side `GEMINI_API_KEY` in `backend/.env`; never expose it through a `VITE_` variable or commit it. See [backend/README.md](backend/README.md), [account-service/README.md](account-service/README.md), [extension/README.md](extension/README.md), and [docs/api-contract.md](docs/api-contract.md) for setup and API details.

## Responsible-use boundaries

Bait reports signals and evidence for human review. It does not declare a person or wallet fraudulent, verify real-world recipient identity, fetch arbitrary websites, authorize payments, or replace independent confirmation through a trusted contact.
