from .math_utils import mod_exp

def encrypt_block(m: int, e: int, n: int) -> int:
    """
    Computes
    c = (m^e) mod n
    using modular exponentiation by squaring
    """
    if m >= n: 
        raise ValueError(f"Block value m ({m}) must be strictly less than modulus n ({n}).")
    return mod_exp(m, e, n)

def decrypt_block(c: int, d: int, n: int) -> int:
    """
    Computes
    m = (c^d) mod n
    using modular expnentiation by squaring
    """
    return mod_exp(c, d, n)
