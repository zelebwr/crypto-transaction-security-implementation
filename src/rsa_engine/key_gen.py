from .math_utils import extended_gcd, mod_inverse, is_prime, get_n_and_totient

def generate_keypair(p: int, q: int, e: int = 65537) -> tuple[tuple[int, int], tuple[int, int], dict]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both p and q must be prime numbers.")
    if p == q: 
        raise ValueError("p and q cannot be equal.")

    n, phi_n = get_n_and_totient(p, q)

    gcd, _, _ = extended_gcd(e, phi_n)

    if gcd != 1:
        e = 3
        gcd, _, _ = extended_gcd(e, phi_n)
        while gcd != 1:
            e += 2
            gcd, _, _ = extended_gcd(e, phi_n)

    d = mod_inverse(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)

    debug_info = {
        "p": p,
        "q": q,
        "n": n,
        "phi_n": phi_n,
        "e": e,
        "d":d
    }

    return public_key, private_key, debug_info
