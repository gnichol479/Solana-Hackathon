# Solana Hackathon — Complete Team Project Briefing

**Project Name:** TBD — The team has not finalized a name.

**Project Category:** AI, Cybersecurity, FinTech, Solana Blockchain

**Team Size:** 4 Developers

**Project Status:** Planning / Early Development

**Main Goal:** Build an AI-powered payment scam detection platform that helps people identify suspicious payment requests before sending money.

---

# 1. The Problem

**People lose money because scammers trick them into sending payments to fraudulent recipients.**

Payment scams happen through emails, invoices, text messages, fake websites, social media, cryptocurrency transactions, and online marketplaces.

Examples include:

- A scammer impersonates a legitimate company and sends a fake invoice.
- Someone receives an email asking them to send money to a changed bank account.
- A fake online seller requests payment for a product they don't intend to deliver.
- A cryptocurrency user is tricked into sending funds to a malicious wallet.
- A criminal compromises a legitimate email account and sends fraudulent payment instructions.

These scams can affect individuals, freelancers, small businesses, and large corporations.

Our project focuses specifically on **detecting suspicious payment requests before money is sent**.

This is not intended to be a general-purpose antivirus or comprehensive phishing protection platform.

# 2. Our Solution

We are developing a payment scam detection platform consisting of two main user interfaces:

**1. Chrome Browser Extension**

A simple browser extension that allows someone to analyze a suspicious payment request while browsing the internet.

**2. Web Application**

A more detailed platform for analyzing invoices, payment requests, suspicious messages, and cryptocurrency wallets.

Both interfaces communicate with the same backend.

The backend determines what type of payment request the user submitted and performs the appropriate security checks.

The platform supports two categories of payment requests:

### Universal Payment Scam Detection

For traditional payment methods, such as bank transfers, PayPal, Venmo, or other payment requests.

The application can examine:

- Suspicious email content
- Potential impersonation
- Unusual urgency or pressure
- Suspicious URLs
- Payment instruction changes
- Inconsistencies in invoices
- Previously approved recipient details, when available
- Other indicators of possible fraud

The application cannot independently access private bank transaction histories or prove that an unfamiliar bank account belongs to a particular company.

### Solana Payment Scam Detection

For cryptocurrency payments involving Solana.

The application performs the same universal checks while additionally examining available public blockchain data.

Possible checks include:

- Wallet transaction history
- Recent wallet activity
- Transaction patterns
- Interactions with known suspicious addresses, when credible intelligence exists
- Wallet ownership signatures, when voluntarily provided
- Known scam reports from external sources
- Potentially suspicious payment instructions

These indicators contribute to an explainable risk assessment.

**Important:** A new wallet is not automatically suspicious, an old wallet is not automatically trustworthy, and a wallet signature proves control of a private key—not a person's real-world identity.

# 3. The Core Concept

The product should feel like **one application**, not two separate products.

Users should not have to understand blockchain to use it.

The system should attempt to identify whether a payment request involves Solana.

If Solana is detected, additional blockchain analysis runs.

If it is a traditional payment request, universal scam detection runs without blockchain analysis.

If the payment method cannot be identified, the system should continue with applicable checks and clearly explain any missing information.

The Chrome extension should look and function the same way regardless of payment method.

The website can show more specialized information based on the payment type.

# 4. Example User Scenarios

## Scenario A: Business Invoice Fraud

A business receives an invoice claiming to be from a legitimate supplier.

The invoice requests a $2,500 bank transfer.

However, a scammer has changed the payment instructions.

The user opens the browser extension and chooses to analyze the invoice.

The application:

1. Extracts the invoice details.
2. Identifies the claimed vendor.
3. Examines the email or document for suspicious information.
4. Compares payment details against previously approved information, if available.
5. Identifies potential inconsistencies.
6. Displays a warning explaining why the payment deserves investigation.

If payment details cannot be independently verified, the system should say so rather than claim the account is fraudulent.

## Scenario B: Solana Cryptocurrency Scam

Someone receives a message asking them to send 100 USDC to a Solana wallet.

They submit the request to the browser extension.

The application:

1. Extracts the wallet address and requested amount.
2. Identifies the payment as potentially involving Solana.
3. Checks whether the address is valid on Solana.
4. Retrieves relevant public blockchain activity.
5. Analyzes suspicious patterns and any available external scam intelligence.
6. Combines blockchain findings with the message's scam indicators.
7. Produces a risk assessment with evidence.

The wallet is not automatically considered safe because no suspicious activity was found.

## Scenario C: Online Marketplace Scam

A person wants to purchase a $300 laptop from an online seller.

The seller sends a suspicious payment request containing urgent language and an unfamiliar payment link.

The buyer submits the request.

The application:

1. Examines the payment message.
2. Inspects the destination URL.
3. Identifies possible scam indicators.
4. Explains why the request may be risky.
5. Recommends independent verification before payment.

This scenario demonstrates how the platform helps everyday people, not just businesses.

# 5. Main Features

## Feature 1: AI Payment Request Analysis

Users can submit payment-related text, emails, invoices, or supported links.

The application extracts structured information such as:

- Claimed sender or business
- Requested payment amount
- Payment method
- Recipient information
- Cryptocurrency wallet addresses
- Payment URLs
- Suspicious statements
- Other relevant details

An AI model assists with extraction and interpretation.

Deterministic code should handle checks such as wallet-address validation, exact address comparisons, domain comparisons, and supported transaction lookups.

The AI should explain suspicious evidence rather than fabricate fraud conclusions.

## Feature 2: Universal Scam Detection

The application examines payment requests for common scam indicators.

Potential indicators include:

- Requests for immediate or secret payments
- Unusual changes to payment instructions
- Suspicious domains
- Impersonated brands
- Unexpected cryptocurrency requests
- Inconsistencies between invoice information and known records

A suspicious signal is not necessarily proof of fraud.

The system should distinguish between known facts, potential warning signs, and information it cannot verify.

## Feature 3: Solana Blockchain Analysis

When a Solana payment request is detected, the backend queries Solana blockchain data.

Potential information includes:

- Whether an address is syntactically valid
- Whether an account exists on the selected network
- Available transaction history
- Recent transfers
- Token activity, when available
- Known interactions with suspicious addresses

The application can explain what the available evidence suggests.

Because public blockchain data is limited, the system must not claim that it can automatically identify the real-world owner of every wallet.

## Feature 4: Browser Extension

The Chrome extension is intended to be the simplest way to use the product.

Users can:

- Open the extension.
- Submit selected text or a payment request.
- Request an analysis.
- Review the resulting warnings.
- Open a detailed report on the website.

The extension should support both traditional and Solana payment requests without separate modes.

For the initial MVP, explicitly user-initiated scanning is preferred over continuously reading emails or browser activity.

The browser extension is **not** expected to execute cryptocurrency transactions.

## Feature 5: Web Application

The website provides additional functionality, including:

- Invoice or document upload
- Text-based analysis
- Fraud warnings
- Detailed explanations
- Identified payment information
- Solana blockchain evidence
- Links to blockchain explorer transactions
- Previous analysis results, if implemented

The website and browser extension should use the same underlying backend.

## Feature 6: Explainable Risk Results

Every analysis should produce a consistent result.

Suggested categories:

**Suspicious:** Significant warning signs or confirmed inconsistencies were detected.

**Needs Verification:** There is insufficient information to verify the recipient or payment request.

**No Major Warnings Detected:** The available checks did not identify significant warning signs.

The third category must never be presented as proof that a payment is completely safe.

Every result should include an explanation and supporting evidence.

# 6. Technical Architecture

The project consists of four main technical components.

### Component A: Website

React or Next.js frontend.

Allows users to submit payment requests and view detailed reports.

### Component B: Chrome Extension

Chrome Manifest V3 extension using HTML, CSS, and JavaScript or TypeScript.

Communicates with the shared backend API.

### Component C: AI Analysis Module

Python-based component responsible for analyzing payment-related content and producing structured findings.

### Component D: Backend & Solana Integration

Python FastAPI backend coordinating requests, providing endpoints, handling blockchain analysis, and returning consistent results.

The architecture can be summarized as:

```text
       CHROME EXTENSION           WEBSITE
              |                     |
              |                     |
              +----------+----------+
                         |
                         v
                    BACKEND API
                         |
             +-----------+-----------+
             |                       |
             v                       v
       AI SCAM ANALYSIS       PAYMENT TYPE CHECK
                                     |
                              Solana payment?
                                /        \
                              YES         NO
                               |           |
                               v           |
                        SOLANA WALLET      |
                          ANALYSIS         |
                               |           |
                               +-----+-----+
                                     |
                                     v
                             COMBINED FINDINGS
                                     |
                                     v
                              RISK ASSESSMENT
                                     |
                                     v
                           WEBSITE OR EXTENSION
```

Universal AI analysis should run for both types of payment requests.

Solana analysis adds blockchain information when applicable.

# 7. Proposed Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Frontend | React / Next.js | Website |
| Styling | Tailwind CSS | Responsive interface |
| Extension | Chrome Manifest V3 | Browser integration |
| Backend | Python + FastAPI | Central API |
| AI | LLM API | Extract and interpret payment requests |
| Blockchain | Solana | Analyze cryptocurrency wallets |
| Solana SDK | Solana Python SDK or compatible RPC client | Blockchain communication |
| Database | PostgreSQL / Supabase | Store scans and approved recipient records if needed |
| Hosting | Vercel + backend hosting | Deployment |
| Version Control | GitHub | Collaboration |

These are recommendations, not mandatory final decisions.

For the initial demo, a database is optional if all analysis can be performed without storing user submissions.

No custom Solana smart contract is required for the current detection-only MVP.

# 8. Four-Person Team Breakdown

## Person 1 — Backend + Solana

**Role: Team Lead, Backend & Solana Developer**

**Difficulty: Advanced**

Backend + Solana is responsible for the core backend, blockchain integration, and connecting the other components.

### Main Responsibilities

1. Create the central FastAPI backend.
2. Define shared API endpoints and response formats.
3. Implement automatic payment-method detection.
4. Connect the application to Solana through RPC.
5. Retrieve public wallet and transaction data.
6. Implement deterministic blockchain-related checks.
7. Integrate the AI analysis module.
8. Combine risk indicators into a final analysis response.
9. Configure backend deployment.
10. Test the full application end to end.

### Expected Deliverables

- Working backend API.
- Live Solana blockchain lookup.
- Integration with the AI module.
- Standardized analysis responses.
- Backend deployment.
- Completed end-to-end demonstration.

### Important Guidance

Use Solana Devnet for test transactions if they are needed. Mainnet public data may be used for read-only analysis when appropriate.

Never store users' private keys or seed phrases.

Do not claim that a wallet is malicious solely because it is new or has unusual transaction activity.

### Definition of Done

Both the website and browser extension can submit a payment request and receive a meaningful analysis response through the backend.

Solana requests additionally return real blockchain evidence when available.

---

## Person 2 — AI & Scam Detection Developer

**Role: Artificial Intelligence / Fraud Analysis**

**Difficulty: Intermediate**

This developer owns the application's intelligent analysis functionality.

### Main Responsibilities

1. Create a module that accepts payment-request text.
2. Extract payment details into structured data.
3. Identify possible phishing and impersonation signals.
4. Detect suspicious payment language.
5. Identify unusual payment instructions.
6. Explain why a payment request may be risky.
7. Return structured findings to the backend.
8. Test the system with legitimate and suspicious examples.

### Expected Deliverables

- Working AI analysis module.
- Structured extraction of payment details.
- Explainable scam indicators.
- Test cases demonstrating different outcomes.
- Clear interface for integration into FastAPI.

### Example Input

```text
URGENT! Your payment is overdue.

Send $500 immediately to the new
payment account below.

Do not contact our accounting office.
```

### Example Output

```json
{
  "payment_method": "unknown",
  "amount": 500,
  "currency": "USD",
  "indicators": [
    "Urgent payment pressure",
    "Unusual instruction not to verify"
  ],
  "explanation": "The message discourages independent verification and requests immediate payment."
}
```

### Important Guidance

The AI developer does not need to build the website, extension, or blockchain integration.

AI should assist with identifying suspicious signals, not serve as the only authority deciding whether somebody is fraudulent.

The model must not invent missing payment details or claim a sender's identity has been verified without evidence.

### Definition of Done

The AI module can analyze different payment messages and return structured findings with understandable explanations.

---

## Person 3 — Website & Dashboard Developer

**Role: Frontend Developer**

**Difficulty: Beginner-Friendly**

This developer owns the main website and user experience.

### Main Responsibilities

1. Create the React or Next.js application.
2. Design a landing page.
3. Build an analysis submission page.
4. Support pasting suspicious payment text.
5. Add document upload functionality when the backend supports it.
6. Build a results dashboard.
7. Display warnings and explanations.
8. Display additional blockchain details for Solana payments.
9. Connect the website to the backend API.
10. Make the interface responsive and easy to navigate.

### Expected Deliverables

- Working website.
- Payment analysis submission form.
- Risk report interface.
- Solana wallet analysis view.
- Backend API integration.
- Deployed frontend.

### Suggested Website Pages

**Home Page**

Explains the product and provides a clear way to begin an analysis.

**Analyze Page**

Allows users to enter or upload a suspicious payment request.

**Results Page**

Displays the overall assessment, supporting evidence, and recommended next steps.

**Solana Details Section**

Appears when blockchain information is relevant.

It may display wallet activity, transaction records, and links to Solana Explorer.

### Important Guidance

The frontend developer can begin with mock API responses while the backend is being built.

The website should never display a payment as guaranteed safe.

The user interface should make sense to people who know nothing about cryptocurrency.

### Definition of Done

A user can submit a payment request through the website and see a clear, understandable report.

---

## Person 4 — Chrome Extension Developer

**Role: Browser Extension Developer**

**Difficulty: Beginner-Friendly**

This developer owns the browser extension that makes the project convenient for everyday users.

### Main Responsibilities

1. Create a Chrome Manifest V3 extension.
2. Build a simple popup interface.
3. Allow users to submit suspicious text.
4. Optionally support analyzing selected webpage text.
5. Send submitted content to the backend API.
6. Receive the backend's analysis response.
7. Display scam indicators and explanations.
8. Provide a link to the detailed website report.
9. Handle loading states and backend errors.
10. Test the extension in Chrome.

### Expected Deliverables

- Installable Chrome extension.
- Functional popup interface.
- Payment-request submission.
- Backend communication.
- Risk warning display.
- Website integration.

### Expected User Experience

1. User encounters a suspicious payment request.
2. User opens the extension.
3. User chooses to analyze the content.
4. Extension sends the request to the backend.
5. Backend performs applicable checks.
6. Extension displays the results.
7. User can open the website for more information.

### Important Guidance

Do not build separate extension interfaces for Solana and non-Solana payments.

The extension should not automatically send money, request private keys, or continuously capture private browsing content.

Start with manual submission. Add browser selection and contextual integrations only after the basic popup works.

### Definition of Done

The extension works in Chrome and can display real backend analysis for both traditional and Solana payment requests.

# 9. Shared API Contract

All four developers should agree on one shared response structure before writing large amounts of code.

The following is a proposed initial API contract.

### Endpoint

```http
POST /api/analyze
```

### Request

```json
{
  "text": "Send 100 USDC to this Solana wallet...",
  "source": "extension"
}
```

### Response

```json
{
  "analysis_id": "demo-001",
  "payment_type": "solana",
  "risk_level": "needs_verification",
  "summary": "Recipient identity could not be verified.",
  "indicators": [
    {
      "type": "unverified_recipient",
      "severity": "warning",
      "message": "The wallet owner has not been independently verified."
    }
  ],
  "payment_details": {
    "amount": 100,
    "currency": "USDC",
    "recipient": null
  },
  "solana_analysis": {
    "performed": true,
    "network": "mainnet-beta",
    "wallet_address": null,
    "transaction_count": null,
    "known_scam_reports": null
  }
}
```

This example represents an incomplete payment request. The missing wallet address and transaction history are intentional.

The final response schema should be adjusted as development progresses.

For traditional payment requests, the Solana analysis should be marked as not performed rather than returning fabricated blockchain information.

### Suggested Backend Endpoints

| Endpoint | Purpose |
|---|---|
| `GET /api/health` | Verify backend availability |
| `POST /api/analyze` | Analyze a payment request |
| `POST /api/analyze-document` | Analyze an uploaded document |
| `GET /api/solana/wallet/{address}` | Retrieve supported wallet analysis |
| `GET /api/analysis/{id}` | Retrieve a previous report, if persistence is enabled |

The extension and website must share the same underlying analysis logic.

# 10. How Risk Assessment Works

The project needs a structured way to combine different observations.

Potential signals include:

**Message Indicators**

- Suspicious urgency
- Pressure not to contact the vendor
- Requests to change payment information
- Impersonation indicators
- Suspicious URLs

**Recipient Indicators**

- Mismatch against previously approved payment details
- Recipient identity cannot be confirmed
- Conflicting sender and recipient information

**Solana Indicators**

- Unusual transaction patterns
- Interactions with credibly identified malicious addresses
- Onchain evidence inconsistent with claims in the payment request
- Missing or unverifiable wallet ownership claims

Not all signals are equally reliable.

The system should not produce an arbitrary fraud probability and present it as a scientifically validated number.

For the MVP, explainable rule-based categories combined with AI-generated descriptions are preferable.

The application should distinguish:

- Confirmed facts
- Suspicious patterns
- Unknown information
- Recommendations for independent verification

# 11. Why Solana?

Solana provides additional investigative capabilities for cryptocurrency payment requests.

Unlike traditional banking systems, Solana exposes public blockchain activity that applications can query.

This can make it possible to examine wallet behavior, historical transactions, and certain relationships between addresses.

Our Solana integration should use real blockchain data rather than simulated wallet history.

However, the blockchain does not automatically reveal a wallet owner's real-world identity.

The current project's principal Solana feature is **pre-payment wallet analysis**.

We are not yet building a payment processing platform, escrow application, or DeFi lending protocol.

Those are possible future extensions, not current requirements.

**Hackathon consideration:** We should not assume that using Solana RPC or USDC automatically qualifies the application for a decentralized-finance prize. Eligibility depends on the event's actual rules.

# 12. Chrome Extension vs. Website

The two user interfaces serve different purposes.

### Chrome Extension

Focus: Quick analysis while browsing.

It should prioritize:

- Simplicity
- Speed
- Clear warnings
- Minimal interaction
- A single analysis workflow

### Website

Focus: Detailed explanation and investigation.

It should prioritize:

- Full reports
- Evidence breakdowns
- Uploaded invoices
- Blockchain transaction details
- Scan history, if supported
- Clear next steps

Both interfaces use identical backend analysis rules.

There should not be two independently implemented fraud detection systems.

# 13. Shared Development Guidelines

All developers should use the same GitHub repository.

Suggested folder structure:

```text
project/
|
|-- frontend/
|   |-- src/
|   |-- components/
|   |-- pages/
|
|-- extension/
|   |-- manifest.json
|   |-- popup.html
|   |-- popup.js
|   |-- styles.css
|
|-- backend/
|   |-- main.py
|   |-- api/
|   |-- services/
|   |   |-- solana.py
|   |   |-- risk.py
|   |-- models/
|
|-- ai/
|   |-- analyzer.py
|   |-- prompts/
|   |-- tests/
|
|-- docs/
|   |-- api-contract.md
|
|-- README.md
|-- .gitignore
```

This is a proposed structure; it can be changed to accommodate the team's tooling.

### Collaboration Expectations

- Use individual branches for development.
- Do not push broken code directly to `main`.
- Do not commit API keys, private keys, or `.env` files.
- Keep component interfaces consistent.
- Test components independently before integration.
- Use mock data when another developer's component is unfinished.
- Document required environment variables.
- Communicate API contract changes to the whole team.

# 14. Development Phases

## Phase 1 — Foundation

Goal: All developers can start independently.

- Initialize GitHub repository.
- Finalize basic API schema.
- Create backend skeleton.
- Create frontend skeleton.
- Create Chrome extension skeleton.
- Create AI module skeleton.
- Provide shared mock responses.

At the end of this phase, everyone should have working starter code.

## Phase 2 — Core Functionality

Goal: Build the independently functioning components.

**Backend + Solana:** Implement backend API and initial Solana RPC queries.

**AI Developer:** Implement extraction and scam indicator detection.

**Website Developer:** Implement submission and reporting interfaces.

**Extension Developer:** Implement text submission and risk-result display.

At the end of this phase, each person should be able to demonstrate their own component.

## Phase 3 — Integration

Goal: Make the components communicate.

- Connect the AI module to FastAPI.
- Connect Solana analysis to FastAPI.
- Connect the website to the API.
- Connect the extension to the API.
- Test common request and response formats.
- Add robust loading and error handling.

At the end of this phase, both interfaces should return actual analysis results.

## Phase 4 — Testing and Improvements

Goal: Improve the quality and reliability of the application.

Test cases should include:

- Legitimate-looking payment request with insufficient verification evidence.
- Suspicious bank transfer instructions.
- Invoice with changed recipient information.
- Solana wallet with normal transaction activity.
- Solana wallet associated with a credible suspicious-activity dataset.
- Payment request with no wallet or recipient details.
- Invalid Solana address.
- AI extraction failure.
- Unavailable blockchain RPC.
- Backend API failure.

Tests should check that the system explains uncertainty rather than inventing conclusions.

## Phase 5 — Final Hackathon Demo

Goal: Demonstrate the project clearly.

Suggested demonstration:

**Demo Part 1 — Universal Scam Detection**

Show a suspicious invoice or payment email.

Open the Chrome extension.

Analyze the request.

Display the warning and explanation.

**Demo Part 2 — Solana Payment Detection**

Show a cryptocurrency payment request.

Use the exact same extension.

The backend recognizes the Solana payment information and investigates the wallet.

Display actual blockchain evidence and explain the resulting assessment.

**Demo Part 3 — Detailed Dashboard**

Open the website and show the expanded report.

Demonstrate how the platform combines AI findings with blockchain evidence.

Conclude by explaining how the product could help protect ordinary people and businesses before money is sent.

# 15. MVP vs. Optional Features

## Required MVP

The minimum complete product should include:

- A working website.
- A working Chrome extension.
- Text-based payment-request analysis.
- AI-assisted extraction and scam indicator identification.
- Automatic payment-method detection.
- Real Solana wallet lookup.
- A consistent, explainable risk assessment.
- A deployed backend.
- A functioning end-to-end demo.

## Optional Features

Only add these after the core application works:

- PDF and image invoice extraction.
- Automatic Gmail invoice detection.
- Email header authentication analysis when headers are accessible.
- Scan history and user accounts.
- Approved-recipient lists.
- External wallet threat-intelligence integration.
- Wallet relationship visualization.
- Phishing URL reputation services.
- Fraud report exports.
- Community-submitted scam reports with abuse protections.
- Wallet ownership verification through digital signatures.
- Solana wallet connection and payment previews.

These features should not delay completion of the core application.

# 16. Important Security and Privacy Requirements

Since this is a security-focused product, our implementation must be careful about the claims it makes.

**Recipient Verification**

A blockchain wallet address does not prove the owner's identity.

A signed message proves someone controls the associated private key.

Real-world identity verification requires additional independent evidence.

**Fraud Assessment**

An unusual transaction pattern does not automatically prove malicious activity.

The application should describe risk indicators instead of making unsupported accusations.

**Privacy**

Invoices and payment requests may contain sensitive information.

Do not publicly log submitted financial documents, email contents, or private customer information.

Avoid permanent storage unless necessary.

**Browser Permissions**

Use the minimum Chrome permissions needed.

Do not continuously collect information from webpages without an appropriate reason and user awareness.

**Blockchain Credentials**

Never request a wallet seed phrase or private key.

Read-only wallet investigation does not require users to connect their own wallets.

**Payment Protection Claims**

The MVP detects and warns about suspicious payments.

It cannot block payments made independently through a bank, exchange, or external wallet.

Only a future integrated payment workflow could enforce restrictions on payments made through that workflow.

**Security Testing**

Use fictional invoices, controlled test cases, and public blockchain data.

Do not make unsupported accusations about actual people or wallets.

# 17. What Makes This Project Different?

Many scam detectors focus on suspicious text or phishing URLs.

Our proposed platform combines traditional scam analysis with additional blockchain investigation when cryptocurrency is involved.

The intended benefits are:

1. One application for both traditional and Solana payment requests.
2. AI-assisted extraction of payment information.
3. Additional blockchain evidence when relevant.
4. Explainable warnings rather than unsupported conclusions.
5. Convenient browser extension access.
6. Detailed reports for users who need further information.

These are intended product features, not claims that the application already outperforms existing fraud detection products.

# 18. Project Priorities

The team should prioritize building a complete, reliable demonstration.

The order of importance is:

1. The system analyzes real user input.
2. The results provide meaningful scam indicators.
3. The extension and website use the same backend.
4. Solana analysis uses real blockchain information.
5. The system communicates uncertainty accurately.
6. The interface is understandable to ordinary users.
7. The finished demo is stable and convincing.

Complex features are less valuable than a complete demonstration that actually works.

# 19. How Teammates Should Use This Briefing With ChatGPT

Each teammate should paste this entire document into their own ChatGPT conversation.

Then explain which team role they are responsible for.

The assistant should:

- Treat this briefing as the shared project specification.
- Focus development assistance on that person's assigned component.
- Keep the shared architecture and API contract in mind.
- Avoid rebuilding components owned by other teammates.
- Prefer beginner-friendly explanations for newer developers.
- Provide clear implementation and testing instructions.
- Ask to inspect existing project files before replacing code.
- Avoid making major architecture changes without coordination.
- Identify dependencies on other teammates.
- Help produce a working, testable component.
- Preserve the project's distinction between traditional payment analysis and additional Solana investigation.

The assistant should not assume all proposed features are implemented.

The current product is a **pre-payment scam detection platform**, not a cryptocurrency exchange or general payment processor.

---

# 20. Final Project Summary

We are building an AI-powered payment scam detection application designed to help individuals and businesses identify suspicious payment requests before sending money.

The product includes a Chrome extension for quick analysis and a website for more detailed investigations.

Both use a shared backend.

Universal scam detection examines potential impersonation, suspicious language, URLs, invoices, and payment instructions.

When a request involves Solana, the backend additionally analyzes available public blockchain information to identify potential wallet-related warning signs.

The project is divided among four developers:

- **Person 1:** Backend & Solana Integration.
- **Person 2:** AI & Scam Detection.
- **Person 3:** Website & Dashboard.
- **Person 4:** Chrome Extension.

Our objective is to demonstrate one consistent user experience for analyzing traditional and cryptocurrency payment scams, with additional Solana-based evidence when available.

**The central promise: Help people recognize suspicious payment requests before they send money.**