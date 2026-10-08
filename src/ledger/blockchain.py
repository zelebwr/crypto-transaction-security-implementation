"""In-memory linked-block simulator; no consensus or payment validation."""

import json
from copy import deepcopy
from time import time

from .transaction import Transaction

__all__ = ["calculate_block_hash", "LedgerManager"]


def calculate_block_hash(block: dict) -> str:
    """Manual FNV-1a 64-bit checksum, NOT a cryptographic hash."""
    content = {key: value for key, value in block.items() if key != "block_hash"}
    raw = json.dumps(content, sort_keys=True, separators=(",", ":")).encode("utf-8")
    value = 14695981039346656037
    for byte in raw:
        value = ((value ^ byte) * 1099511628211) & ((1 << 64) - 1)
    return f"{value:016x}"


class LedgerManager:
    def __init__(self):
        self.chain: list[dict] = []
        self._pending_transactions: list[Transaction] = []
        self._tx_ids: set[str] = set()
        self._append_block([])  # Genesis block.

    @property
    def pending_transactions(self) -> list[dict]:
        """Return a snapshot; callers cannot change the actual queue."""
        return [tx.to_dict() for tx in self._pending_transactions]

    def _append_block(self, transactions: list[dict]) -> dict:
        block = {
            "block_index": len(self.chain),
            "timestamp": int(time()),
            "previous_hash": self.chain[-1]["block_hash"] if self.chain else "0" * 16,
            "transactions": deepcopy(transactions),
        }
        block["block_hash"] = calculate_block_hash(block)
        self.chain.append(block)
        return deepcopy(block)

    def add_transaction(self, transaction: Transaction) -> None:
        if not isinstance(transaction, Transaction):
            raise ValueError("Gunakan objek Transaction")
        if not self.validate_chain():
            raise ValueError("Ledger tidak valid; transaksi dibatalkan")
        if transaction.tx_id in self._tx_ids:
            raise ValueError("ID transaksi duplikat")
        self._pending_transactions.append(transaction)
        self._tx_ids.add(transaction.tx_id)

    def commit_block(self) -> dict:
        if not self.validate_chain():
            raise ValueError("Ledger tidak valid; commit dibatalkan")
        if not self._pending_transactions:
            raise ValueError("Tidak ada transaksi untuk dikomit")
        block = self._append_block(self.pending_transactions)
        self._pending_transactions.clear()
        return block

    def validate_chain(self) -> bool:
        """Check block layout, checksums, links, and transaction schemas."""
        if not self.chain:
            return False
        previous_hash = "0" * 16
        seen_ids: set[str] = set()
        try:
            for index, block in enumerate(self.chain):
                if type(block["block_index"]) is not int or block["block_index"] != index:
                    return False
                if type(block["timestamp"]) is not int or block["timestamp"] < 0:
                    return False
                if block["previous_hash"] != previous_hash:
                    return False
                if block["block_hash"] != calculate_block_hash(block):
                    return False
                if not isinstance(block["transactions"], list):
                    return False
                if index == 0 and block["transactions"]:
                    return False
                if index > 0 and not block["transactions"]:
                    return False
                for tx in block["transactions"]:
                    if not isinstance(tx["encrypted_payload"], list):
                        return False
                    Transaction(
                        tx["tx_id"], tx["sender_address"], tx["recipient_address"],
                        (tx["rsa_public_key_used"]["e"], tx["rsa_public_key_used"]["n"]),
                        tuple(tx["encrypted_payload"]),
                    )
                    if tx["tx_id"] in seen_ids:
                        return False
                    seen_ids.add(tx["tx_id"])
                previous_hash = block["block_hash"]
        except (KeyError, TypeError, ValueError, OverflowError):
            return False
        return True
