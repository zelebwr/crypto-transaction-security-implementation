import sys
from src.rsa_engine.key_gen import generate_keypair
from src.rsa_engine.math_utils import is_prime
from src.ledger.blockchain import LedgerManager
from src.interface.donor_view import render_donor_view
from src.interface.ledger_view import render_ledger_view
from src.interface.creator_view import render_creator_view


def get_prime_input(prompt: str, default: int) -> int:
    """Prompt user for a prime number, falling back to a default if empty."""
    while True:
        user_val = input(f"{prompt} [Default: {default}]: ").strip()
        if not user_val:
            return default
        if user_val.isdigit():
            val = int(user_val)
            if is_prime(val):
                return val
            print("  ❌ Input is not a prime number! Please enter a valid prime.")
        else:
            print("  ❌ Invalid input! Please enter an integer.")


def setup_creator_wallet():
    """Prompt user for RSA parameters and initialize creator keypair."""
    print("\n" + "=" * 50)
    print(" [SETUP] CREATOR WALLET INITIALIZATION")
    print("=" * 50)
    print("Select prime numbers p and q (must be distinct primes > 15):")
    
    p = get_prime_input("Enter prime p", default=61)
    while True:
        q = get_prime_input("Enter prime q", default=53)
        if q != p:
            break
        print("  ❌ q cannot be equal to p! Choose a different prime.")

    e_input = input("Enter public exponent e [Default: 17]: ").strip()
    e = int(e_input) if e_input.isdigit() else 17

    try:
        public_key, private_key, debug_info = generate_keypair(p, q, e=e)
        print("\n  ✅ RSA Keypair Generated Successfully!")
        print(f"  • Modulus n      : {debug_info['n']} (p={p}, q={q})")
        print(f"  • Totient phi(n) : {debug_info['phi_n']}")
        print(f"  • Public Key (e) : {public_key[0]}")
        print(f"  • Private Key (d): {private_key[0]}")
        return public_key, private_key
    except Exception as err:
        print(f"  ❌ Key generation failed: {err}")
        sys.exit(1)


def prompt_donor_input() -> tuple[str, str, str]:
    """Interactively collect donor details."""
    print("\n" + "=" * 50)
    print(" [DONOR] CREATE SEALED TIP")
    print("=" * 50)
    
    donor_name = input("Enter your name/alias [e.g., Alice]: ").strip() or "Anonymous"
    amount = input("Enter donation amount in IDR [e.g., 50000]: ").strip() or "10000"
    message = input("Enter private message/reward note: ").strip() or "Keep up the great work!"
    
    sender_addr = f"0x{donor_name.replace(' ', '')}Wallet"
    plaintext_note = f"DONOR: {donor_name} | AMOUNT: {amount} IDR | MSG: {message}"
    
    return sender_addr, plaintext_note


def main():
    # Initialize Persistent System State
    ledger = LedgerManager()
    
    # Step 1: Wallet Setup
    print("=" * 65)
    print(" CRYPTOGRAPHY INDEPENDENT CREATOR MICRO-DONATION NETWORK")
    print("               (RSA SEALED TIPPING PROTOCOL)")
    print("=" * 65)
    
    public_key, private_key = setup_creator_wallet()
    recipient_addr = "0xCreatorWalletMain"

    # Interactive Menu Loop
    while True:
        print("\n" + "=" * 50)
        print(" MAIN MENU")
        print("=" * 50)
        print(" [1] Send a Sealed Donation (Donor View)")
        print(" [2] View Blockchain Explorer (Ledger View)")
        print(" [3] Access Creator Dashboard (Decrypt Incoming Tips)")
        print(" [4] Re-initialize Creator Wallet Keys")
        print(" [5] Exit Application")
        
        choice = input("\nSelect an option [1-5]: ").strip()

        if choice == "1":
            sender_addr, plaintext_note = prompt_donor_input()
            tx = render_donor_view(
                sender_addr=sender_addr,
                recipient_addr=recipient_addr,
                plaintext_note=plaintext_note,
                public_key=public_key
            )
            ledger.add_transaction(tx)
            committed_block = ledger.commit_block()
            print(f"\n  ✅ Block #{committed_block['block_index']} Mined and Saved to Ledger!")

        elif choice == "2":
            if len(ledger.chain) <= 1:
                print("\n  ℹ️ No donation blocks mined yet (only Genesis Block exists).")
            else:
                for block in ledger.chain[1:]:  # Skip Genesis block
                    render_ledger_view(block)

        elif choice == "3":
            if len(ledger.chain) <= 1:
                print("\n  ℹ️ No transactions available to decrypt.")
            else:
                print(f"\n[Dashboard] Attempting decryption using Active Private Key (d={private_key[0]}, n={private_key[1]})...")
                for block in ledger.chain[1:]:
                    for tx in block["transactions"]:
                        tx_key = tx["rsa_public_key_used"]
                        
                        # Check if transaction was encrypted with the active wallet key
                        if tx_key["e"] == public_key[0] and tx_key["n"] == public_key[1]:
                            encrypted_payload = tx["encrypted_payload"]
                            render_creator_view(encrypted_payload, private_key)
                        else:
                            print("\n" + "-" * 50)
                            print(f" 🔒 [TX: {tx['tx_id']}] SEALED PAYLOAD (UNREADABLE)")
                            print("-" * 50)
                            print(f" Payload Key : (e={tx_key['e']}, n={tx_key['n']})")
                            print(f" Active Key  : (e={public_key[0]}, n={public_key[1]})")
                            print(" Status      : Cannot decrypt — encrypted for a different creator keypair.")

        elif choice == "4":
            public_key, private_key = setup_creator_wallet()
            print("\n  🔑 Active Creator Wallet Keypair updated.")
            print("  (Note: Historical blockchain blocks remain preserved on-chain!)")

        elif choice == "5":
            print("\nExiting application. Goodbye!")
            break

        else:
            print("\n  ❌ Invalid choice! Please select an option from 1 to 5.")


if __name__ == "__main__":
    main()
