from src.ledger.transaction import new_transaction, Transaction

def render_donor_view(
    sender_addr: str, 
    recipient_addr: str, 
    plaintext_note: str, 
    public_key: tuple[int, int]
) -> Transaction:
    e, n = public_key
    print("\n" + "=" * 50)
    print(" [1] DONOR CONSOLE: SEALED TIP CREATION")
    print("=" * 50)
    print(f" Sender Address   : {sender_addr}")
    print(f" Recipient Address: {recipient_addr}")
    print(f" Plaintext Message: \"{plaintext_note}\"")
    print(f" Target Public Key: (e={e}, n={n})")

    # Creates Transaction object and automatically encrypts payload via rsa_core
    tx = new_transaction(
        sender_address=sender_addr,
        recipient_address=recipient_addr,
        plaintext=plaintext_note,
        public_key=public_key
    )

    print(f"\n -> Transaction ID Generated: {tx.tx_id}")
    print(f" -> Encrypted Ciphertext Payload (c_i < {n}):")
    print(f"    {list(tx.encrypted_payload[:10])}... (Total {len(tx.encrypted_payload)} blocks)")

    return tx
