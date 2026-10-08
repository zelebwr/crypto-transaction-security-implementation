---
type: project-hub
tags:
status: In Progress
tech_stack: [Python]
repo_url: https://github.com/zelebwr/crypto-transaction-security-implementation
exclude_tasks: true
---

# Cryptography independent Creator Micro-Donation Network


## Project Overview / Objectives

### Project Overview: Independent Creator Micro-Donation Network (RSA Sealed Tipping Protocol)

This project implements a decentralized, peer-to-peer tipping network where supporters can send digital donations and private messages to online content creators (streamers, open-source developers, writers, and digital artists) using a **Sealed Transfer** blockchain model.

---

### Real-Life Study Case

#### The Context

Online creators rely heavily on direct fan support through platforms like Patreon, Ko-fi, or Streamlabs. However, current solutions present two major issues:

1. **Centralized Platform Inefficiencies:** Traditional platforms charge 5%–12% in commission and processing fees and can freeze funds arbitrarily.
2. **Public Blockchain Privacy Dilemma:** Moving donations to a standard public blockchain eliminates middleman fees, but exposes all donor identities, exact tip amounts, email addresses for reward claims, and personal messages publicly on the ledger.

#### The Problem Solved

By introducing **RSA Sealed Transfers** onto a simulated blockchain, the public ledger records transaction validity and routing without exposing sensitive supporter messages or reward codes to public blockchain explorers.

---

### Project Objectives & Purpose

- **Demonstrate Pure RSA Operations:** Implement from-scratch mathematical functions for RSA key generation, block chunking, encryption, and decryption without relying on built-in cryptographic libraries or frameworks.
- **On-Chain Data Confidentiality:** Protect private supporter communications (e.g., email addresses, private appreciation messages, physical mailing addresses for merchandise rewards) on a transparent distributed ledger.
- **Simulate Blockchain Core Principles:** Showcase how unencrypted public headers can co-exist with encrypted execution payloads within an immutable block ledger.

---

### End-to-End System Architecture & RSA Lifecycle

```
[ DONOR / SUPPORTER ]
        |
        |--- 1. Enter Plaintext Note: "From: Alice | Email: alice@mail.com | Message: Love your work!"
        |--- 2. Fetch Creator's RSA Public Key (e, n)
        |--- 3. Chunk text -> ASCII integers (m_i < n)
        |--- 4. Encrypt: c_i = (m_i)^e mod n
        v
[ SIMULATED BLOCKCHAIN LEDGER ]
        |
        |--- Public Header : Sender, Recipient ID, Timestamp, Block Hash
        |--- Encrypted Payload: [c_1, c_2, c_3, ...] (Unreadable Ciphertext Array)
        v
[ CREATOR DASHBOARD ]
        |
        |--- 1. Read Encrypted Transaction Payload from Ledger
        |--- 2. Apply Private Key (d, n)
        |--- 3. Decrypt: m_i = (c_i)^d mod n
        |--- 4. Convert ASCII integers back to Plaintext String

```

#### Step 1: Creator Key Generation (Wallet Initialization)

The creator initializes their creator wallet profile by generating an RSA keypair:

1. Select two prime numbers, $p$ and $q$.
2. Calculate modulus: $n = p \times q$.
3. Compute Euler's totient: $\phi(n) = (p - 1) \times (q - 1)$.
4. Choose public exponent $e$ such that $\gcd(e, \phi(n)) = 1$.
5. Calculate private exponent $d$ using the Extended Euclidean Algorithm:

$$d \cdot e \equiv 1 \pmod{\phi(n)}$$

6. **Public Wallet Address:** Published as $(e_{\text{creator}}, n_{\text{creator}})$.
7. **Private Wallet Key:** Kept secret as $(d_{\text{creator}}, n_{\text{creator}})$.

#### Step 2: Payload Assembly & Encryption (Donor Side)

When a fan sends a tip:

1. **Plaintext Construction:** The donor enters their support message:

```text
"DONOR: Alice | AMOUNT: 50000 IDR | REWARD_EMAIL: alice@mail.com | MSG: Great stream!"

```

2. **ASCII Integer Chunking:** The text is converted into byte/ASCII code integers $m_1, m_2, \dots, m_k$, where each $m_i < n_{\text{creator}}$.
3. **Modular Exponentiation Encryption:** Each integer block is encrypted using the creator's public key:

$$c_i \equiv (m_i)^{e_{\text{creator}}} \pmod{n_{\text{creator}}}$$

4. **Transaction Broadcasting:** The transaction object containing public routing parameters and the encrypted payload array $[c_1, c_2, \dots, c_k]$ is broadcast to the network.

#### Step 3: Block Storage (Simulated Blockchain)

The system appends the transaction into an unconfirmed block, computes the block hash, and commits it to the distributed ledger array.

#### Step 4: Payload Decryption (Creator Dashboard)

The creator accesses their private dashboard:

1. The dashboard extracts the ciphertext array $[c_1, c_2, \dots, c_k]$ from incoming block transactions.
2. Applies the creator's private key parameters $(d_{\text{creator}}, n_{\text{creator}})$ via modular exponentiation:

$$m_i \equiv (c_i)^{d_{\text{creator}}} \pmod{n_{\text{creator}}}$$

3. Reconstructs the original ASCII integers into cleartext to reveal the private donor details and reward email.

---

### Data Schema (Transaction JSON Model)

```json
{
  "block_index": 4,
  "previous_hash": "0000a3f892c...",
  "timestamp": 1728387000,
  "transaction": {
    "tx_id": "TX_DONATION_1092",
    "sender_address": "0xDonorWalletPublic",
    "recipient_address": "0xCreatorWalletPublic",
    "rsa_public_key_used": {
      "e": 65537,
      "n": 3233
    },
    "encrypted_payload": [
      "1024", "0892", "2041", "0119", "2830", "1544"
    ]
  }
}

```

---

### Demonstrating Implementation for Report & Presentation

| Program Component        | Functionality                                                         | What to Display in Output / Terminal Demo                                                  |
| ------------------------ | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| **RSA Math Engine**      | Pure mathematical routines: GCD, Extended GCD, Modular Exponentiation | Print $p$, $q$, modulus $n$, totient $\phi(n)$, public exponent $e$, private exponent $d$. |
| **Data Encoding**        | Text-to-Integer and Integer-to-Text mapping                           | Display raw input string $\rightarrow$ ASCII array $\rightarrow$ Ciphertext array.         |
| **Blockchain Simulator** | Block creation, transaction appending, hash generation                | Display public block viewer showing unreadable cipher integers $[1024, 0892, \dots]$.      |
| **Creator Interface**    | Decryption triggering using private key $d$                           | Display decrypted cleartext note successfully recovered on the creator's view.             |

---

## Architecture & Environment
- **Local Port:**
- **Production URL:**
- **Key Dependencies:**

---
