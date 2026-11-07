# Bait feature status

## Available in the static website

- Existing landing, manual analysis and risk reports preserved.
- Browser-local screenshot OCR with review/edit before submission.
- Browser-local QR decoding; validated Solana Pay transfer fields and safe plain-text handling for unknown QR formats. Transaction-request URLs are displayed without fetching or executing them.
- PNG/JPEG/WEBP previews, drag/drop, size/type/decoded-dimension checks, errors and processing status. Image bytes are never sent to a server.
- Conservative text extraction for amount/currency, explicit Solana network, wallet candidates, explicit recipient/company fields, purpose, deadline, references and URLs. Unreadable/missing values stay unknown. Review extraction; it is not verification.
- Actual address-byte validation, exact comparison against an opt-in fictional Northstar Design registry, dated evidence and clear simulated-match/mismatch status.
- Unknown merchants remain unverified. There are no independently authenticated real merchant records.
- Local URL structure findings for known-brand strings outside their official domain, IP hosts, embedded credentials, non-HTTPS and punycode. No website fetch, comprehensive typo detection, or reputation provider.
- Navigation to scanner, recipient comparison, blockchain lookup, account security and report history.

## Integrated services

- Email/password account registration/login, logout, session expiration.
- WebAuthn passkey registration/login with actual server-side cryptographic verification. Device biometrics are controlled by the operating system.
- Six-digit PIN creation/reset, confirmation UI, server Argon2id hashing, account/IP throttles and stronger reauthentication for security changes.
- HttpOnly sessions, Origin and CSRF checks, private opt-in report storage/deletion.
- Read-only Solana public RPC lookup with explicit network selection, live balances, signatures, timestamps and explorer links.
- Optional schema-validated AI phishing adapter; requires a server API key. Each supported finding includes a quote, explanation/category and next action.
- Password recovery requires SMTP delivery configuration.
- The local integration launcher starts the analysis/Solana backend, account service and Vite frontend together. Document uploads accept PDFs server-side; images are OCR'd in the browser and only reviewed text is sent to analysis.

The published static website still needs deployed backend origins and any required AI/SMTP configuration. The local `.env.local` is intentionally ignored by Git; `frontend/.env.example` documents the three integration settings. The Sites static host alone cannot run the Python services.

## Verification

17 frontend tests pass, and the shared backend/account contract additions compile cleanly. The synchronous backend detection/risk suite passes 6 tests; a pure account-service report-contract test passes. The full ASGI/TestClient suites remain incompatible with the local Python 3.14 Windows runtime because requests hang before assertions, so live Uvicorn checks cover the service boundary instead. Live checks passed for both health endpoints, JSON analysis, PDF multipart extraction, browser-OCR handoff, unsupported upload rejection, live Devnet analysis and wallet lookup, registration/login/logout, CSRF-protected report save/list/delete surface, and passkey challenge issuance. Browser checks successfully rendered analysis, OCR review, recipient comparison, live Devnet evidence, account security and report history with no console errors. No real biometric identity or real business identity has been verified.

Read `account-service/README.md` for deployment conditions and privacy limits. This is a hackathon implementation, not an audited production security service.
