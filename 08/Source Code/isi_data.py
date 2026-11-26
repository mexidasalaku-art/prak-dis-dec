import sqlite3

DB_FILE = "toko-produk.db"

DATA = [
    ("PRD001", "Keyboard Mekanik", 450000.0, 25, True),
    ("PRD002", "Mouse Wireless", 175000.5, 40, True),
    ("PRD003", "Monitor 24 Inci", 1850000.0, 0, False),
    ("PRD004", "Headset Gaming", 320000.75, 15, True),
    ("PRD005", "Webcam Full HD", 275000.0, 0, False),
]

conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS produk (
        id INTEGER PRIMARY KEY,
        kode CHAR(6),
        nama VARCHAR(50),
        harga FLOAT,
        stok INT,
        tersedia BOOLEAN
    )
    """
)

cur.execute("DELETE FROM produk")
cur.executemany(
    "INSERT INTO produk (kode, nama, harga, stok, tersedia) VALUES (?, ?, ?, ?, ?)",
    DATA,
)
conn.commit()

for row in cur.execute("SELECT * FROM produk"):
    print(row)

conn.close()
print("Selesai: 5 data berhasil diisikan.")