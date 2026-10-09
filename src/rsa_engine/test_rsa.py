from src.rsa_engine.key_gen import generate_keypair
from src.rsa_engine.rsa_core import encrypt_block,decrypt_block

p = 61
q = 53

# 2. Generate RSA Keypair
public_key, private_key, debug_info = generate_keypair(p, q, e=17)

print("=== RSA KEY GENERATION PARAMETERS ===")
for key, val in debug_info.items():
    print(f"{key}: {val}")

e, n = public_key
d, _ = private_key

# 3. Single Block Encryption Cycle (e.g., ASCII character 'A' = 65)
message_char_code = 65  # 'A'

ciphertext = encrypt_block(m=message_char_code, e=e, n=n)
decrypted_code = decrypt_block(c=ciphertext, d=d, n=n)

print("\n=== RSA ENCRYPTION / DECRYPTION TEST ===")
print(f"Original Code : {message_char_code} ('{chr(message_char_code)}')")
print(f"Encrypted     : {ciphertext}")
print(f"Decrypted Code: {decrypted_code} ('{chr(decrypted_code)}')")

assert message_char_code == decrypted_code, "Decryption failed!"
print("\nSuccess: Math engine successfully verified!")
