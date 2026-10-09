"""Encode UTF-8 text as one byte per RSA plaintext block."""

__all__ = ["text_to_ascii_chunks", "ascii_chunks_to_text"]


def text_to_ascii_chunks(text: str, n: int) -> list[int]:
    """ASCII has the same byte values; UTF-8 also supports Unicode text."""
    if not isinstance(text, str):
        raise ValueError("Pesan harus berupa string")
    if type(n) is not int or n <= 255:
        raise ValueError("Encoding satu byte per blok membutuhkan n > 255")
    return list(text.encode("utf-8"))


def ascii_chunks_to_text(chunks: list[int]) -> str:
    """Reconstruct text from decrypted byte values, preserving zero bytes."""
    if any(type(value) is not int or not 0 <= value <= 255 for value in chunks):
        raise ValueError("Blok hasil dekripsi harus integer dalam rentang 0–255")
    return bytes(chunks).decode("utf-8")
