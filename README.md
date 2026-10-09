# Cryptography Independent Creator Micro-Donation Network

Made by Kelompok 16:

1. Jonathan Zelig Sutopo—5027241047
2. M.Atha Tajuddin—5027241093
3. Hafidzal Raynandra—5026231117

---


## Data Schema Rules

```jsdon
```json
{
  "block_header": {
    "block_index": 1,
    "timestamp": 1728387000,
    "previous_hash": "0000000000000000",
    "block_hash": "a4f892c109e..."
  },
  "transaction": {
    "tx_id": "TX_DONATION_001",
    "sender_address": "0xDonorWalletPublic",
    "recipient_address": "0xCreatorWalletPublic",
    "rsa_public_key_used": {
      "e": 65537,
      "n": 3233
    },
    "encrypted_payload": [1024, 892, 2041, 119]
  }
}
```


---

## Sources

1. [Pollard's RHO Algorithm](https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm) or [Pollard RHO Algorithm for Integer Factorization and Discrete Logarithm Problem](https://www.researchgate.net/profile/Nagaratna-Hegde/publication/281979237_Pollard_RHO_Algorithm_for_Integer_Factorization_and_Discrete_Logarithm_Problem/links/5d947fb092851c33e94e9c4a/Pollard-RHO-Algorithm-for-Integer-Factorization-and-Discrete-Logarithm-Problem.pdf?_tp=eyJjb250ZXh0Ijp7ImZpcnN0UGFnZSI6InB1YmxpY2F0aW9uIiwicGFnZSI6InB1YmxpY2F0aW9uIn19)
2. [Extended Euclidean Algorithm](https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm) or [A Practical Guide to the Extended Euclid Algorithm](https://wiki.math.ntnu.no/_media/tma4155/2010h/euclid.pdf)
3. 

