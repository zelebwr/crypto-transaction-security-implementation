# Ledger Simulator

Ledger Sprint 1 memakai list blok di memori. Tidak ada library kriptografi
di modul ledger; enkripsi didelegasikan ke perhitungan RSA manual anggota 1.

## Alur dan tanggung jawab file

1. `encoder.py`: teks menjadi byte UTF-8, satu byte per blok RSA, lalu
   mengembalikan byte hasil dekripsi menjadi teks. Teks ASCII tetap menghasilkan
   nilai ASCII yang sama. Modulus harus `n > 255` agar setiap byte memenuhi `m < n`.
2. `transaction.py`: membuat transaksi dengan alamat publik, public key creator,
   dan ciphertext. Plaintext dan private key tidak disimpan dalam transaksi.
3. `blockchain.py`: membuat genesis block, mengantrekan transaksi, menolak ID
   duplikat, membuat blok baru, serta memeriksa checksum dan tautan antarblok.
4. `__init__.py`: mengekspor fungsi dan kelas untuk integrasi dari `src.ledger`.

## Penggunaan dari folder root proyek

```python
from src.ledger import LedgerManager, new_transaction, ascii_chunks_to_text
from src.rsa_engine.rsa_core import generate_keypair, decrypt_block

public_key, private_key = generate_keypair(61, 53, 17)
tx = new_transaction(
    sender_address="0xDonor",
    recipient_address="0xCreator",
    plaintext="DONOR: Alice | AMOUNT: 50000 IDR | MSG: Terima kasih!",
    public_key=public_key,
)

ledger = LedgerManager()
ledger.add_transaction(tx)
block = ledger.commit_block()

print(block)
print("Chain valid:", ledger.validate_chain())

d, n = private_key
stored_tx = ledger.chain[-1]["transactions"][0]
message = ascii_chunks_to_text([
    decrypt_block(c, d, n) for c in stored_tx["encrypted_payload"]
])
print("Pesan creator:", message)
```

**Dependensi yang belum selesai:** modul RSA saat ini kosong. Contoh di atas
baru dapat dijalankan setelah `generate_keypair(p, q, e)`,
`encrypt_block(m, e, n)`, dan `decrypt_block(c, d, n)` diimplementasikan.
`new_transaction()` menampilkan `NotImplementedError` jika fungsi enkripsi
belum tersedia atau masih mengembalikan `None` dari stub `pass`.
Encoder dan penyimpanan objek `Transaction` dapat digunakan secara terpisah.

## Bentuk blok dan batas simulasi

- Blok memiliki `block_index`, `timestamp`, `previous_hash`, `transactions`,
  dan `block_hash`. `transactions` adalah list agar satu blok menampung banyak
  transaksi. Genesis berada di indeks 0 dan tidak memiliki transaksi.
- `pending_transactions` memberikan salinan antrean; gunakan `add_transaction()`
  untuk menambah transaksi dan `commit_block()` untuk menyimpannya. Commit tanpa
  transaksi ditolak. Nilai hasil commit juga merupakan salinan blok.
- `chain` tetap terbuka untuk inspeksi dan demonstrasi perubahan data.
  `validate_chain()` mendeteksi perubahan yang tidak disertai perhitungan ulang
  checksum, ketidaksesuaian tautan blok, dan skema transaksi tidak valid.
- `block_hash` memakai checksum FNV-1a 64-bit yang dihitung manual, **bukan hash
  kriptografis**. Ini tidak menjamin immutability atau mencegah penulisan ulang
  seluruh rantai. Jika tugas mensyaratkan hash kriptografis, perlu implementasi
  SHA-256 manual sebagai penggantinya.
- Validasi public key di ledger hanya memeriksa bentuk dan rentang dasar;
  pemilihan prima dan syarat RSA seperti `gcd(e, phi) = 1` milik crypto engine.
- ID transaksi berurutan berlaku dalam satu proses dan kembali dari awal saat
  program diulang. Ledger belum disimpan ke file, belum memiliki konsensus,
  tanda tangan pengirim, pemeriksaan saldo, atau transfer dana sungguhan.
- RSA kecil tanpa padding dan encoding satu byte per blok hanya untuk demo.

## Referensi awal

- [Lazy Annotations Python](https://realpython.com/python-annotations/)

- [Proof-of-Work Blockchain](https://www.geeksforgeeks.org/python/implementing-the-proof-of-work-algorithm-in-python-for-blockchain-mining/)

- [Elipsis usage,three dots,type hinting](https://www.geeksforgeeks.org/python/what-is-three-dots-or-ellipsis-in-python3/)


- [Build simple blockchain](https://levelup.gitconnected.com/building-a-simple-blockchain-in-python-973cb6fa265b)

- [Build private & public key blockchain implementation](https://medium.com/jin-system-architect/introduction-to-blockchain-technology-and-implemented-by-using-python-part-1-9d1fa7f158c7)


## Real-case

- [Blockchain Implementation with Pyhton,Ethereum-Node](https://riacheruvu.medium.com/tech-dive-series-understanding-and-implementing-blockchain-with-python-4-f373f441039f)


## Git PR Strategy

```
# 1. Make a new branch for later PR (jangan langsung ke main)
git checkout -b feat/ledger-module

# 2. Kerjakan ledger...

# 3. Commit
git add src/ledger/ data/ledger_state.json
git commit -m "feat(ledger): implement block creation, transaction append, and hashing"

# 4. Push
git push -u origin feat/ledger-module

```
