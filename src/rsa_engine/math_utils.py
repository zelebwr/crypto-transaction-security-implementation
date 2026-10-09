def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def extended_gcd(a:int, b: int) -> tuple[int, int, int]:
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def get_n_and_totient(p: int, q: int) -> tuple[int, int]:
    n = p * q
    phi_n = ((p - 1) * (q - 1))
    return n, phi_n

def mod_inverse(e: int, phi: int) -> int:
    gcd, x, _ = extended_gcd(e, phi)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist: e({e}) and phi ({phi}) are not coprime.")
    # Using module phi_n to ensure d is always a positive integer
    return x % phi

def mod_exp(base: int, exp: int, mod: int) -> int:
    result = 1 
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

