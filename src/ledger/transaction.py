from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from typing import Any

from .encoder import text_to_ascii_chunks

__all__ = ["PublicKey", "Transaction", "next_tx_id", "new_transaction"]

PublicKey = tuple[int, int]
_tx_counter = count(1)


def next_tx_id() -> str:
    """Generate an ID unique within this running process."""
    return f"TX_DONATION_{next(_tx_counter):03d}"


def _validate_public_key(public_key: PublicKey) -> None:
    if (
        not isinstance(public_key, tuple)
        or len(public_key) != 2
        or any(type(value) is not int for value in public_key)
    ):
        raise ValueError("Public key harus tuple integer (e, n)")
    e, n = public_key
    if e <= 1 or n <= 255:
        raise ValueError("Public key membutuhkan e > 1 dan n > 255")


@dataclass(frozen=True)
class Transaction:
    tx_id: str
    sender_address: str
    recipient_address: str
    rsa_public_key_used: PublicKey
    encrypted_payload: tuple[int, ...]

    def __post_init__(self) -> None:
        for value in (self.tx_id, self.sender_address, self.recipient_address):
            if not isinstance(value, str) or not value.strip():
                raise ValueError("ID transaksi dan alamat wajib berupa string terisi")
        _validate_public_key(self.rsa_public_key_used)
        _, n = self.rsa_public_key_used
        if not isinstance(self.encrypted_payload, tuple) or not self.encrypted_payload:
            raise ValueError("Payload harus tuple ciphertext yang tidak kosong")
        if any(type(c) is not int or not 0 <= c < n for c in self.encrypted_payload):
            raise ValueError("Ciphertext harus integer dalam rentang 0 <= c < n")

    def to_dict(self) -> dict[str, Any]:
        """Return a fresh JSON-compatible representation without plaintext."""
        e, n = self.rsa_public_key_used
        return {
            "tx_id": self.tx_id,
            "sender_address": self.sender_address,
            "recipient_address": self.recipient_address,
            "rsa_public_key_used": {"e": e, "n": n},
            "encrypted_payload": list(self.encrypted_payload),
        }


def new_transaction(
    sender_address: str,
    recipient_address: str,
    plaintext: str,
    public_key: PublicKey,
) -> Transaction:
    """Encrypt a donor message with the creator's public key."""
    for address in (sender_address, recipient_address):
        if not isinstance(address, str) or not address.strip():
            raise ValueError("Alamat pengirim dan penerima wajib diisi")
    if not isinstance(plaintext, str) or not plaintext.strip():
        raise ValueError("Pesan wajib berupa string terisi")
    _validate_public_key(public_key)
    e, n = public_key
    chunks = text_to_ascii_chunks(plaintext, n)

    # Import lazily: encoding and ledger storage can run before RSA is ready.
    from ..rsa_engine import rsa_core

    encrypt_block = getattr(rsa_core, "encrypt_block", None)
    if not callable(encrypt_block):
        raise NotImplementedError("Implementasikan rsa_core.encrypt_block(m, e, n)")
    ciphertext = tuple(encrypt_block(m, e, n) for m in chunks)
    if any(c is None for c in ciphertext):
        raise NotImplementedError("rsa_core.encrypt_block masih berupa stub/pass")

    return Transaction(
        next_tx_id(), sender_address, recipient_address, public_key, ciphertext,
    )
