# Payment Lens frontend

Person 3's React website. Payment Lens is a temporary product name; change it when the team agrees on branding.

## Run

Install Node.js 22 or later, then open a terminal in `frontend`:

```sh
npm install
npm run dev
```

Open the local address printed in the terminal. `npm run build` creates the deployment folder `dist`. `npm test` checks report handling and demo behavior.

If using the project-local Node downloaded during setup, run `../.tools/node-v22.14.0-win-x64/node.exe ../.tools/node-v22.14.0-win-x64/node_modules/npm/bin/npm-cli.js run dev` after adding that Node directory to your terminal PATH.

## Connect Person 1's backend

Copy `.env.example` to `.env.local` and set `VITE_API_BASE_URL` to the backend origin (for example `http://localhost:8000`). Restart the development server. Configure backend CORS to allow the frontend origin. Production should use an HTTPS backend.

The website sends `POST /api/analyze` with `{ "text": "...", "source": "website" }` and displays the briefing's shared response structure. Accepted risk levels: `suspicious`, `needs_verification`, `no_major_warnings_detected`. The backend should avoid exposing raw submissions in logs and return understandable failures.

Optional uploads: set `VITE_ENABLE_DOCUMENT_UPLOAD=true` only after coordinating `POST /api/analyze-document` with Person 1. The current multipart contract sends `file` plus optional `text`; the backend must validate file type and size and implement extraction. The browser allows PDF, PNG, JPG up to 10 MB.

Without an API origin, all results are visibly labeled demonstrations using simple local text rules. Demo mode does not run AI or Solana RPC. It does not invent wallet history, amounts, or recipient identities. No submissions are stored by this frontend. Requests go to the configured backend only when a user submits.

## Deploy

For Vercel or another static host, set the project root to `frontend`, build command to `npm run build`, and output directory to `dist`. Add the API origin as `VITE_API_BASE_URL` before building. This app uses hash navigation, so no route rewrites are needed. Google Fonts are optional; system fonts are used when unavailable.

## New scanner and verification tools

The website now includes browser-local screenshot OCR, QR decoding, editable extracted text, automatic payment fields, limited URL structure warnings, and recipient wallet comparison. Open **Screenshot & QR** and choose **Try demo screenshot** or **Try mismatch QR**. These examples generate actual images and run the real image-processing pipeline. Review the extracted text, then continue to analysis or recipient comparison.

The fictional **Northstar Design** merchant registry is opt-in. Its reserved `.example` domain and wallet association are synthetic, and every match/mismatch is labeled as a demo. No authenticated real merchant registry is connected; unknown businesses remain unverified. Neither arbitrary websites nor QR links are fetched automatically.

OCR assets and the English language model are bundled under `public/ocr`, so uploaded screenshots stay in the browser. Tesseract.js and its runtime/model licenses are recorded in `public/ocr/NOTICE.md`. Large image processing may be slower on mobile. OCR can misread addresses: users must review before proceeding.

## Account, history, AI and blockchain integration

The Account Security, Previous Reports and Blockchain Lookup screens use real API endpoints when configured. They do not simulate a successful login, identity, balance or AI result. Without a deployed backend they show an explicit service notice.

A separately implemented service lives in `../account-service/` with setup/deployment instructions. It includes email/password login, server-verified WebAuthn, salted PIN hashing with lockouts, CSRF-protected HttpOnly sessions, private opt-in report storage/deletion, read-only Solana RPC, and an optional AI adapter. Coordinate adoption with Person 1. Password recovery requires SMTP, and live AI requires a server-side API key. The static Sites deployment does not execute Python.

For local account integration, use `VITE_API_BASE_URL=http://localhost:8000`, run the account service, and open the frontend at **http://localhost:5173**. Use the same frontend hostname as the service's configured Origin/RP ID. The local analysis-method selector remains available without an AI key.

See `../docs/feature-status.md` for implemented features and limits. Guest reports stay in memory; account reports are saved only when the user chooses Save. No Chrome extension is implemented here.
