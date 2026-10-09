from src.rsa_engine.rsa_core import decrypt_block
from src.ledger.encoder import ascii_chunks_to_text

def render_creator_view(encrypted_payload: list[int], private_key: tuple[int, int]) -> str:
    d, n = private_key
    print("\n" + "=" * 50)
    print(" [3] CREATOR PRIVATE DASHBOARD")
    print("=" * 50)
    print(f" Applying Private Key (d={d}, n={n})...")

    # Step A: Decrypt each ciphertext integer: m_i = (c_i)^d mod n
    decrypted_chunks = [decrypt_block(c, d, n) for c in encrypted_payload]
    print(f" -> Recovered ASCII Integer Blocks:")
    print(f"    {decrypted_chunks[:10]}...")

    # Step B: Reconstruct string from ASCII codes
    restored_text = ascii_chunks_to_text(decrypted_chunks)
    print(f"\n -> Decrypted Cleartext Message:")
    print(f"    \"{restored_text}\"")

    return restored_text
