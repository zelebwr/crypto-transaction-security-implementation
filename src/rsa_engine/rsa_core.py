def generate_keypair(p: int, q: int, e: int = 65537) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Computes RSA keys from scratch.
    Returns: ((e, n), (d, n))
    """
    pass

def encrypt_block(m: int, e: int, n: int) -> int:
    """
    Computes
    c = (m^e) mod n
    using modular exponentiation by squaring
    """
    pass

def decrypt_block(c: int, d: int, n: int) -> int:
    """
    Computes
    m = (c^d) mod n
    using modular expnentiation by squaring
    """
    pass
