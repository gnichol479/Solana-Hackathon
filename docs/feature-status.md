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

## Implemented but requires backend deployment/configuration

- Email/password account registration/login, logout, session expiration.
- WebAuthn passkey registration/login with actual server-side cryptographic verification. Device biometrics are controlled by the operating system.
- Six-digit PIN creation/reset, confirmation UI, server Argon2id hashing, account/IP throttles and stronger reauthentication for security changes.
- HttpOnly sessions, Origin and CSRF checks, private opt-in report storage/deletion.
- Read-only Solana public RPC lookup with explicit network selection, live balances, signatures, timestamps and explorer links.
- Optional schema-validated AI phishing adapter; requires a server API key. Each supported finding includes a quote, explanation/category and next action.
- Password recovery requires SMTP delivery configuration.

The published website has no backend address or API key configured. It makes account and RPC service availability explicit. It does not simulate successful login or live blockchain/AI results. Deploying the Python service to a persistent host and setting the frontend API origin is still required. The Sites static host alone cannot run this service.

## Verification

13 frontend tests and 10 backend tests passed. Automated tests cover payment extraction, exact fixture matches/mismatches/unknown recipients, invalid addresses, Solana Pay parsing, real generated QR decoding, upload validation and local URL indicators. Backend tests cover actual cryptographic WebAuthn registration/assertion signatures, challenge replay/expiry rejection, password/PIN authentication, lockouts, CSRF, session expiration, cross-user report protection, recovery-token revocation, unavailable RPC behavior and removal of unsupported AI quotes. Tests use generated credentials, local synthetic records and mocked remote service failures. A separate live Devnet request successfully returned a SOL balance, 10 recent signatures and a lookup timestamp. Browser checks successfully recognized the demo screenshot, decoded the demo QR, handed its requested wallet to comparison, and displayed the labeled match/mismatch outcomes. The scanner layout was inspected at 390px width. No real biometric identity or real business identity has been verified.

Read `account-service/README.md` for deployment conditions and privacy limits. This is a hackathon implementation, not an audited production security service.
