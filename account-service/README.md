# Optional account and evidence service

This separate FastAPI service adds real email/password, passkey, PIN and report endpoints without replacing Person 1's backend. Coordinate integration before adopting it as the shared API. The hosted static website does **not** run Python; it requires an independently deployed backend or a same-origin reverse proxy.

## Local development

Install Python 3.13 and dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:LENS_INSECURE_LOCAL='1'
$env:LENS_ORIGIN='http://localhost:5173'
$env:LENS_RP_ID='localhost'
.\.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8002
```

Set `VITE_ACCOUNT_API_BASE_URL=http://localhost:8002` in the frontend's `.env.local`, restart the frontend, and browse **http://localhost:5173** (use the same hostname throughout). The service accepts only the exact configured Origin for writes. Run `python -m pytest -q` to run the isolated security tests. Project-local installed dependencies are also available at `../.tools/backend-env/Scripts/python.exe` on this development machine.

Environment variables are read from the process environment; `.env.example` is a reference, not automatically loaded. Database files must stay out of Git.

## Production

Deploy with a persistent, access-restricted SQLite volume and **one process** for the hackathon. Use PostgreSQL and a shared rate limiter for multiple replicas. Put the service behind HTTPS, set `LENS_ORIGIN` to the frontend origin and `LENS_RP_ID` to its hostname, and leave `LENS_INSECURE_LOCAL` unset. Use a same-site backend domain or a same-origin `/api` proxy: the HttpOnly, Secure, SameSite=Lax cookie intentionally does not support third-party cookie deployments. Configure your reverse proxy to limit JSON bodies to 100 KB and reject inappropriate forwarded-host headers. The rate limiter uses the direct peer address; configure a trusted proxy explicitly before using a forwarded client IP. Use TLS and encrypted storage/backups from your hosting provider.

The browser never receives password/PIN hashes or private API credentials. Sessions expire after one hour by default, rotate on login, and are revoked on logout and password reset. Every authenticated mutation requires its session CSRF token and a trusted Origin. PINs use salted Argon2id hashes with five login attempts per account per 15-minute window; additional IP limits apply. Security changes require password/passkey login, and PIN changes additionally require the current password. There is no payment authorization endpoint.

Passkey challenges expire in two minutes, are single-use, and registration is bound to its authenticated session. Server verification checks origin, relying-party ID, credential signature, counter, and user-verification flags. Native device Face ID/Windows Hello behavior still needs testing on the target device. Accounts are not labeled email-verified; email ownership confirmation is not implemented.

SMTP configuration is required for recovery email. Recovery tokens are hashed, expire in 15 minutes, and are single-use; password reset also clears the PIN and revokes sessions. No reset tokens are returned through the API or logs.

Saved reports are opt-in, schema-validated and limited to 100 per account. Raw images and original message text are not stored. Extracted report fields can contain sensitive information; saved reports are accessible and deletable only by their owner. SQLite deletion removes records from application access; normal file-level remnants/backups follow your storage provider's retention policy.

## Live analysis dependencies

`GET /api/solana/wallet/{address}?network=devnet` performs read-only calls to the configured fixed public Solana RPC origins. It returns SOL balance, up to 10 signatures/timestamps, and up to 50 legacy SPL Token account balances. No arbitrary website or QR endpoint is fetched. A network must be chosen because addresses do not encode a cluster. RPC errors return 503; no cached or invented results are substituted. Token-2022 balances and scam reputation data are not included.

`POST /api/analyze` is an optional AI adapter. Set `GEMINI_API_KEY`, `GEMINI_MODEL`, and `GEMINI_BASE_URL` on the server; otherwise it returns a clear unavailable response. It uses Gemini structured JSON output, validates responses with Pydantic, treats payment content only as untrusted user data, and drops findings with quotes absent from the input. No model has tools or URL-fetching access. These measures reduce prompt-injection exposure; they do not prove immunity. Results are indicators requiring review. The live AI service has not been exercised without an API key; tests mock provider output.

Identity comparison is deliberately conservative: only the frontend's explicitly labeled fictional merchant fixture can produce a demo match or mismatch. A real authenticated merchant registry and real merchant onboarding are not connected. Unknown identities remain unverified.

The extension can keep using Person 1's existing API. If adopting this service for extension submissions, define an explicit extension Origin allowlist with the team rather than disabling Origin checks.
