# RAG Knowledge Base - USDC Digital Bank

This document serves as the vector database (RAG) for the digital bank's AI assistant. It contains KYC guidelines, transaction workflows, and frequently asked questions (FAQ) regarding operations with the USDC stablecoin.

---

## 1. KYC (Know Your Customer) and Compliance Guidelines

### Account Verification Levels
* **Level 1 (Basic):** Daily limit of \$5,000 USDC. Requires full name, date of birth, email, and validated phone number.
* **Level 2 (Verified):** Daily limit of \$50,000 USDC. Requires a photo of an identity document (ID card, Driver's License, or Passport) and a biometric selfie.
* **Level 3 (Pro):** No strict operational limits. Requires updated proof of residence (last 90 days) and proof of source of funds for high-volume deposits.

### Anti-Money Laundering (AML) Red Flags
* **Structuring (Smurfing):** Multiple transactions of values just below the \$10,000 USDC monitoring threshold.
* **Inconsistency:** Account movements that are incompatible with the income declared in the user's profile.
* **High-Risk Accounts:** Attempts to send or receive funds linked to sanctioned wallets or cryptocurrency mixers (e.g., Tornado Cash).

---

## 2. USDC Transaction Workflow

### Deposit (Fiat to USDC)
1. **Request:** The user requests a deposit in fiat currency (e.g., via Pix or bank transfer).
2. **Conversion:** The bank receives the funds and issues the equivalent amount in USDC at an exact 1:1 ratio.
3. **Credit:** The USDC balance becomes available in the user's digital account within 10 minutes after fiat clearance.

### Sending USDC (On-Chain / Blockchain)
1. **Supported Networks:** The bank operates natively via the **Ethereum** network to ensure scalability.
2. **Address Validation:** The AI or the app must validate that the destination address (a 42-character public key starting with `0x`) belongs to the same network selected by the user.
3. **Internal Custody:** Transfers between users of the same digital bank are instantaneous and have zero fees (off-chain).

### Withdrawal (USDC to Fiat)
1. **Reverse Conversion:** The user sells their USDC within the app.
2. **Settlement:** The bank burns or retains the USDC and initiates the fiat transfer to the bank account under the exact same ownership as the user.

---

## 3. Digital Bank FAQ (Frequently Asked Questions)

### Q1: What is USDC and how secure is it?
USD Coin (USDC) is a stablecoin pegged to the US dollar at a 1:1 ratio. It is issued by Circle and is fully audited, ensuring that every token in circulation is backed by an equivalent dollar in cash reserves or short-term US Treasury bonds.

### Q2: My USDC transaction is stuck. What should I do?
* **Internal Transfer:** Occurs instantaneously. Verify if the sender's balance has been debited.
* **External Transfer (Blockchain):** Request the Transaction Hash (TxID). Use a block explorer (such as PolygonScan or Arbiscan) to check the network processing status. If it is "Pending", the blockchain network is congested and you must wait.

### Q3: Can I cancel a USDC transfer that has already been sent?
**No.** Once a transaction is confirmed and recorded on the blockchain, it becomes irreversible. Always double-check the destination address and the selected network before confirming with your password.

### Q4: What fees are applied by the bank?
* **Account Opening and Maintenance:** Free.
* **Internal Transfers:** Zero fees.
* **Fiat Withdrawals and Deposits:** A flat fee of 0.5% on the converted amount.
* **Sending to External Wallets:** A fluctuating network fee (gas) passed on entirely to the user.
