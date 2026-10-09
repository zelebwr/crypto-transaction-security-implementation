from src.rsa_engine.key_gen import generate_keypair
from src.ledger.blockchain import LedgerManager
from src.interface.donor_view import render_donor_view
from src.interface.ledger_view import render_ledger_view
from src.interface.creator_view import render_creator_view

def main():
    print("=" * 60)
    print(" CRYPTOGRAPHY INDEPENDENT CREATOR MICRO-DONATION NETWORK")
    print("               (RSA SEALED TIPPING PROTOCOL)")
    print("=" * 60)

    # 1. SETUP: Creator generates RSA wallet keys
    p, q = 61, 53
    public_key, private_key, debug_info = generate_keypair(p, q, e=17)
    
    print("\n[KEYGEN] Creator Wallet Initialized:")
    print(f"  p={debug_info['p']}, q={debug_info['q']}, n={debug_info['n']}, phi={debug_info['phi_n']}")
    print(f"  Public Key (e, n) : {public_key}")
    print(f"  Private Key (d, n): {private_key}")

    # 2. DONOR STAGE: Build & encrypt tip payload
    donor_note = "DONOR: Alice | AMOUNT: 50000 IDR | MSG: Keep up the great work!"
    tx = render_donor_view(
        sender_addr="0xDonorAliceWallet",
        recipient_addr="0xCreatorBobWallet",
        plaintext_note=donor_note,
        public_key=public_key
    )

    # 3. LEDGER STAGE: Add transaction & commit block
    ledger = LedgerManager()
    ledger.add_transaction(tx)
    block = ledger.commit_block()
    
    render_ledger_view(block)

    # 4. CREATOR STAGE: Retrieve from chain & decrypt payload
    stored_tx = block["transactions"][0]
    encrypted_payload_from_chain = stored_tx["encrypted_payload"]
    
    restored_note = render_creator_view(encrypted_payload_from_chain, private_key)

    # Sanity Check Assertion
    assert restored_note == donor_note, "Decryption verification failed!"
    print("\n" + "=" * 60)
    print(" SUCCESS: End-To-End RSA Sealed Transfer Pipeline Operational!")
    print("=" * 60)

if __name__ == "__main__":
    main()
