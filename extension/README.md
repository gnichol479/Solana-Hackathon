# Bait Chrome Extension

Manifest V3 popup for quick, user initiated payment request analysis. It matches the website's dark forest background, mint fish mascot, and careful risk language.

## Load in Chrome

1. Open `chrome://extensions`.
2. Turn on **Developer mode**.
3. Choose **Load unpacked** and select this `extension` folder.
4. Open the extension and use the gear button to enter your backend URL and website URL.
5. Choose **Save connection** and grant access to that backend origin.
6. Paste text or select text on a page and use **Use selection**, then choose **Analyze request**.

For local development, enter `http://localhost:8000` for the API and `http://localhost:5173` for the site. For a deployed backend, enter its HTTPS origin. The backend must allow the extension origin in CORS (`chrome-extension://<extension-id>`); a stable Chrome extension ID is needed for deployment configuration.

## Shared backend contract

The popup sends `POST /api/analyze` with `{ "text": "...", "source": "extension" }` and displays the shared response's `risk_level`, `summary`, `indicators`, `payment_details`, `payment_type`, and `solana_analysis`. See [`../docs/api-contract.md`](../docs/api-contract.md).

## Privacy and permissions

- `activeTab` and `scripting` are used only after the user presses **Use selection**. No page is monitored or read in the background.
- Backend access is optional and requested only for the origin the user configures. The extension submits only after the user presses **Analyze request**.
- There is no wallet connection, transaction signing, payment action, or request for seed phrases or private keys.
- Request text is not written to extension storage.
- The popup uses system font fallbacks; it does not load remote fonts or other remote assets.

The report is decision support. “No major warnings detected” is not a safety guarantee, and public Solana data does not establish wallet ownership.
