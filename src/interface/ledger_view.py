def render_ledger_view(block: dict):
    print("\n" + "=" * 50)
    print(" [2] PUBLIC BLOCKCHAIN EXPLORER (ON-CHAIN STATE)")
    print("=" * 50)
    print(f" Block Index  : {block['block_index']}")
    print(f" Timestamp    : {block['timestamp']}")
    print(f" Block Hash   : {block['block_hash']}")
    print(f" Previous Hash: {block['previous_hash']}")
    print("-" * 50)
    
    for tx in block["transactions"]:
        print(" Transaction Details:")
        print(f"   TX ID            : {tx.get('tx_id')}")
        print(f"   Sender           : {tx.get('sender_address')}")
        print(f"   Recipient        : {tx.get('recipient_address')}")
        print(f"   Public Key Used  : {tx.get('rsa_public_key_used')}")
        payload = tx.get('encrypted_payload', [])
        print(f"   Encrypted Payload: {payload[:6]}... (Sealed, total {len(payload)} blocks)")
