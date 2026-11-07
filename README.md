This project is for Solana Hackathon 2026

## Website — Person 3

The React website is in `frontend/`. On Windows, double-click `start-website.cmd`, then open the local link shown in the terminal.

It includes a landing page, request analysis, screenshot OCR, QR decoding, payment extraction, recipient wallet comparison and a Solana evidence section. Merchant examples are fictional and clearly labeled. See [frontend setup and integration instructions](frontend/README.md) and [feature status](docs/feature-status.md).

An optional [account and evidence service](account-service/README.md) implements account security and protected reports without replacing Person 1's backend. Online login, AI and blockchain tools require a deployed backend connection. On this development machine, `start-account-service.cmd` launches the installed local service; follow its README to connect the frontend.

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

Phantom Help Center

Then enable Devnet:
Go to Settings → Developer Settings.
Turn on Testnet Mode.
Select Solana Devnet. 

Phantom Help Center
