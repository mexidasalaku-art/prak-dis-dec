# Praktikum Minggu MODUL 08 - Arsitektur Microservices untuk Sistem Terdistribusi


| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi | 
| **Topik** | Arsitektur Microservices untuk Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 | 
| **Kelas** | IF-1 |

---

#  TUJUAN PRAKTIKUM


---
#  DASAR TEORI

---
#  PEMBAHASAN PRAKTIKUM
### 1.1 Install uv

```python
winget install --id=astral-sh.uv -e
```
<img width="721" height="293" alt="01" src="https://github.com/user-attachments/assets/3d5cc144-aa21-44fe-8981-67f6305a1f95" />

#### Pembahasan

<p align="justify">Perintah winget install --id=astral-sh.uv -e ini berhasil memperbarui uv, package manager Python buatan Astral, yang sebelumnya sudah terpasang di komputermu. Winget mendeteksi paket lama, lalu mengunduh versi 0.13.10 (14,9 MB) dari GitHub, memverifikasi hash installer, mengekstrak arsipnya, dan memasang ulang sehingga alias uv, uvx, dan uvw terdaftar di command line. Proses diakhiri dengan pesan "Successfully installed", artinya kamu sekarang bisa langsung menjalankan uv dari terminal untuk mengelola paket dan virtual environment Python dengan cepat. Dependensi Microsoft.VCRedist.2015+.x64 juga disebutkan sebagai prasyarat, dan biasanya sudah ada di Windows.</p>

```python
uv --version
```

<img width="471" height="96" alt="02" src="https://github.com/user-attachments/assets/469200cc-bd48-41c8-9b8b-37ccf40f4353" />

#### Pembahasan

<p align="justify">uv --version di terminal yang menampilkan uv 0.13.9 (build 6b2d39dcc, tanggal 2026-11-17, x86_64-pc-windows-msvc). Versi ini sedikit lebih lama daripada 0.13.10 yang baru saja dipasang lewat winget di gambar sebelumnya, jadi kemungkinan jendela terminal ini masih memakai sesi lama yang belum memuat pembaruan, atau alias uv masih mengarah ke instalasi sebelumnya. Coba tutup lalu buka kembali terminal dan jalankan uv --version lagi. Kalau masih tampil 0.13.9, cek lokasi yang dipakai dengan where uv.</p>

### 1.2 Buat workspace dan pin Python 3.14

```python
uv python install 3.14
uv python list
```

<img width="904" height="433" alt="03_1 2" src="https://github.com/user-attachments/assets/d4d6f417-3cb8-478b-9e45-a9fffcc91f15" />

#### Pembahasan

<p align="justify">Perintah uv python install 3.14 menjawab bahwa Python 3.14 sudah terpasang, lalu uv python list menampilkan daftar interpreter Python yang dikenali uv. Versi yang sudah ada di komputermu ditandai dengan path lengkap, yaitu CPython 3.15.0, beberapa versi 3.14 (3.14.8 dan 3.14.4, baik yang dikelola uv di folder AppData\Roaming\uv\python maupun instalasi Python biasa), serta Python 3.13.0 dari Laragon. Sisanya, seperti 3.16.0a2, 3.15.2, 3.14.10, 3.12 sampai 3.8, PyPy, dan GraalPy, bertanda <download available>, artinya belum terpasang tetapi bisa diunduh uv kapan saja. Karena yang terpasang cukup banyak, kamu bisa mengunci versi untuk proyek praktikum dengan uv python pin 3.14 atau memakai uv venv --python 3.14 agar tidak tertukar antar instalasi.</p>


```python
uv python pin 3.14
```

<img width="468" height="67" alt="04" src="https://github.com/user-attachments/assets/c4061f8a-48ba-4b90-8140-719bc8807fa1" />

#### Pembahasan

<p align="justify">Perintah uv python pin 3.14 berhasil memperbarui file .python-version di folder modul praktikum, dari isi sebelumnya C:\path\dari\kolom\kanan\python.exe menjadi 3.14. Isi lama itu sebenarnya path contoh yang tidak valid (kemungkinan tersalin dari teks petunjuk), jadi pembaruan ini justru memperbaikinya. Mulai sekarang, setiap perintah uv di folder ini, seperti uv venv, uv run, atau uv sync, akan memakai Python 3.14 secara konsisten dan tidak lagi tertukar dengan instalasi 3.15 atau 3.13 yang ada di komputermu.</p>


```python
type .python-version
python --version
```

<img width="469" height="56" alt="05" src="https://github.com/user-attachments/assets/178235a3-991d-46ea-a49c-d733a38b3ac2" />

#### Pembahasan

<p align="justify">Perintah type .python-version menampilkan isi file .python-version di folder modul praktikum, yaitu 3.14. Ini mengonfirmasi bahwa uv python pin 3.14 sebelumnya benar-benar tersimpan, dan path contoh yang tidak valid tadi sudah terganti. Dengan begitu, perintah uv seperti uv venv, uv run, dan uv sync di folder ini akan otomatis memakai Python 3.14, sehingga proyek praktikummu siap dilanjutkan ke tahap pembuatan environment.</p>

### 1.3 Buat dan aktifkan environment

```python
uv venv
.venv\Scripts\activate.bat
where python
```

<img width="735" height="240" alt="06_1 3" src="https://github.com/user-attachments/assets/cab6ab8d-6dfb-4b04-9387-6584e8a31361" />

#### Pembahasan

<p align="justify">Perintah uv venv membuat virtual environment .venv di folder modul dengan CPython 3.14.8, sesuai versi yang sebelumnya dikunci lewat .python-version. Karena .venv sudah ada, uv menanyakan apakah ingin menggantinya dan kamu menjawab yes, sehingga environment lama ditimpa dengan yang baru. Setelah diaktifkan lewat .venv\Scripts\activate.bat, prompt berubah menjadi (MODUL), dan hasil where python menunjukkan entri pertama adalah .venv\Scripts\python.exe di folder modul, tanda bahwa environment sudah aktif dan mengalahkan instalasi Python lain (Laragon 3.13, Python 3.15, dan alias WindowsApps). Sekarang paket apa pun yang dipasang dengan uv pip install akan masuk ke environment ini saja, sehingga proyek praktikummu tetap terisolasi.</p>

### 1.4 Install FastAPI dan SQLModel

Paket FastAPI dan SQLModel dipasang dengan perintah berikut.

```python
uv pip install "fastapi[standard]" sqlmodel
```

```python
Resolved 61 packages in 2.95s
Prepared 6 packages in 2.14s
░░░░░░░░░░░░░░░░░░░░ [0/61] Installing wheels...                     warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 61 packages in 5.61s
 + agent-detector==2.0.0
 + annotated-doc==0.0.7
 + annotated-types==0.8.0
 + anyio==4.16.0
 + certifi==2026.11.20
 + charset-normalizer==3.5.3
 + click==8.5.1
 + colorama==0.4.6
 + detect-installer==0.2.1
 + dnspython==2.9.2
 + email-validator==2.4.0
 + fastapi==0.165.0
 + fastapi-cli==0.0.34
 + fastapi-cloud-cli==0.28.0
 + fastar==0.12.0
 + googleapis-common-protos==1.76.0
 + h11==0.16.0
 + httpcore==1.0.9
 + httpcore2==2.16.2
 + httptools==0.9.0
 + httpx==0.28.1
 + httpx2==2.16.2
 + idna==3.20
 + jinja2==3.1.6
 + markdown-it-py==4.3.0
 + markupsafe==3.0.4
 + mdurl==0.1.2
 + opentelemetry-api==1.45.2
 + opentelemetry-exporter-http-transport==0.66b2
 + opentelemetry-exporter-otlp-common==0.66b2
 + opentelemetry-exporter-otlp-proto-common==1.45.2
 + opentelemetry-exporter-otlp-proto-http==1.45.2
 + opentelemetry-proto==1.45.2
 + opentelemetry-sdk==1.45.2
 + opentelemetry-semantic-conventions==0.66b2
 + protobuf==7.36.2
 + pydantic==2.14.4
 + pydantic-core==2.50.5
 + pydantic-extra-types==2.11.1
 + pydantic-settings==2.16.3
 + pygments==2.21.0
 + python-dotenv==1.2.4
 + python-multipart==0.0.34
 + pyyaml==6.0.4
 + requests==2.34.2
 + rich==15.0.0
 + rich-toolkit==0.20.6
 + rignore==0.8.1
 + sentry-sdk==3.0.1
 + shellingham==1.5.4
 + sqlalchemy==2.1.9
 + sqlmodel==0.0.50
 + starlette==1.10.0
 + truststore==0.10.5
 + typer==0.29.2
 + typing-extensions==4.16.0
 + typing-inspection==0.4.5
 + urllib3==2.8.0
 + uvicorn==0.54.0
 + watchfiles==1.3.0
 + websockets==17.4
```

#### Pembahasan

<p align="justify">Output ini menunjukkan uv berhasil menyelesaikan dan memasang 61 paket ke dalam .venv hanya dalam sekitar 5,6 detik. Daftar paketnya mengindikasikan kamu memasang FastAPI beserta ekosistemnya: fastapi dan fastapi-cli, server uvicorn dengan websockets dan watchfiles, validasi data lewat pydantic, ORM sqlmodel dengan sqlalchemy, serta httpx dan requests untuk klien HTTP. Ada pula paket OpenTelemetry dan sentry-sdk yang ikut terpasang sebagai dependensi bawaan. Peringatan "Failed to hardlink files" tidak berbahaya, karena cache uv dan folder proyek berada di drive berbeda (kemungkinan C: dan D:), sehingga uv menyalin file secara penuh dan hanya sedikit lebih lambat. Kalau ingin peringatan itu hilang, jalankan set UV_LINK_MODE=copy sebelum perintah uv. Setelah ini, kamu bisa langsung menjalankan aplikasi dengan fastapi dev atau uvicorn main:app --reload.</p>


<p align="justify">Proses instalasi Python dilakukan menggunakan uv dengan versi 3.14.4. Sebelum memulai instalasi, terlebih dahulu dilakukan pengecekan terhadap daftar versi Python yang tersedia dan dikenali oleh uv melalui perintah berikut.</p>

```python
uv pip list
```

```python
Package                                  Version
---------------------------------------- ----------
agent-detector                           2.0.0
annotated-doc                            0.0.7
annotated-types                          0.8.0
anyio                                    4.16.0
certifi                                  2026.11.20
charset-normalizer                       3.5.3
click                                    8.5.1
colorama                                 0.4.6
detect-installer                         0.2.1
dnspython                                2.9.2
email-validator                          2.4.0
fastapi                                  0.165.0
fastapi-cli                              0.0.34
fastapi-cloud-cli                        0.28.0
fastar                                   0.12.0
googleapis-common-protos                 1.76.0
h11                                      0.16.0
httpcore                                 1.0.9
httpcore2                                2.16.2
httptools                                0.9.0
httpx                                    0.28.1
httpx2                                   2.16.2
idna                                     3.20
jinja2                                   3.1.6
markdown-it-py                           4.3.0
markupsafe                               3.0.4
mdurl                                    0.1.2
opentelemetry-api                        1.45.2
opentelemetry-exporter-http-transport    0.66b2
opentelemetry-exporter-otlp-common       0.66b2
opentelemetry-exporter-otlp-proto-common 1.45.2
opentelemetry-exporter-otlp-proto-http   1.45.2
opentelemetry-proto                      1.45.2
opentelemetry-sdk                        1.45.2
opentelemetry-semantic-conventions       0.66b2
protobuf                                 7.36.2
pydantic                                 2.14.4
pydantic-core                            2.50.5
pydantic-extra-types                     2.11.1
pydantic-settings                        2.16.3
pygments                                 2.21.0
python-dotenv                            1.2.4
python-multipart                         0.0.34
pyyaml                                   6.0.4
requests                                 2.34.2
rich                                     15.0.0
rich-toolkit                             0.20.6
rignore                                  0.8.1
sentry-sdk                               3.0.1
shellingham                              1.5.4
sqlalchemy                               2.1.9
sqlmodel                                 0.0.50
starlette                                1.10.0
truststore                               0.10.5
typer                                    0.29.2
typing-extensions                        4.16.0
typing-inspection                        0.4.5
urllib3                                  2.8.0
uvicorn                                  0.54.0
watchfiles                               1.3.0
websockets                               17.4
```

#### Pembahasan

<p align="justify">Output ini adalah hasil uv pip list yang menampilkan 61 paket di dalam .venv, dan daftarnya sama persis dengan yang baru dipasang pada langkah sebelumnya, sehingga instalasi terkonfirmasi berhasil dan lengkap. Paket intinya adalah fastapi 0.165.0 dengan starlette sebagai fondasi web, uvicorn sebagai server, pydantic 2.14.4 untuk validasi data, serta sqlmodel dan sqlalchemy untuk akses database. Sisanya adalah dependensi pendukung seperti httpx, requests, jinja2, python-dotenv, python-multipart, rich, typer, serta rangkaian opentelemetry dan sentry-sdk yang ikut terpasang otomatis. Karena python-multipart dan email-validator sudah ada, proyekmu siap menangani form, upload file, dan validasi email tanpa instalasi tambahan. Langkah berikutnya adalah membuat file main.py lalu menjalankannya dengan fastapi dev.</p>

```python
uv pip freeze > requirements.txt
type requirements.txt
```

```python
agent-detector==2.0.0
annotated-doc==0.0.7
annotated-types==0.8.0
anyio==4.16.0
certifi==2026.11.20
charset-normalizer==3.5.3
click==8.5.1
colorama==0.4.6
detect-installer==0.2.1
dnspython==2.9.2
email-validator==2.4.0
fastapi==0.165.0
fastapi-cli==0.0.34
fastapi-cloud-cli==0.28.0
fastar==0.12.0
googleapis-common-protos==1.76.0
h11==0.16.0
httpcore==1.0.9
httpcore2==2.16.2
httptools==0.9.0
httpx==0.28.1
httpx2==2.16.2
idna==3.20
jinja2==3.1.6
markdown-it-py==4.3.0
markupsafe==3.0.4
mdurl==0.1.2
opentelemetry-api==1.45.2
opentelemetry-exporter-http-transport==0.66b2
opentelemetry-exporter-otlp-common==0.66b2
opentelemetry-exporter-otlp-proto-common==1.45.2
opentelemetry-exporter-otlp-proto-http==1.45.2
opentelemetry-proto==1.45.2
opentelemetry-sdk==1.45.2
opentelemetry-semantic-conventions==0.66b2
protobuf==7.36.2
pydantic==2.14.4
pydantic-core==2.50.5
pydantic-extra-types==2.11.1
pydantic-settings==2.16.3
pygments==2.21.0
python-dotenv==1.2.4
python-multipart==0.0.34
pyyaml==6.0.4
requests==2.34.2
rich==15.0.0
rich-toolkit==0.20.6
rignore==0.8.1
sentry-sdk==3.0.1
shellingham==1.5.4
sqlalchemy==2.1.9
sqlmodel==0.0.50
starlette==1.10.0
truststore==0.10.5
typer==0.29.2
typing-extensions==4.16.0
typing-inspection==0.4.5
urllib3==2.8.0
uvicorn==0.54.0
watchfiles==1.3.0
websockets==17.4
```

#### Pembahasan

<p align="justify">Output ini adalah hasil uv pip freeze (atau pip freeze), yaitu daftar 61 paket di .venv dengan format nama==versi yang sama persis dengan hasil uv pip list sebelumnya. Format ini sering dipakai sebagai isi requirements.txt agar environment bisa dibuat ulang di komputer lain atau oleh rekan satu kelompok praktikum. Kamu bisa menyimpannya dengan uv pip freeze > requirements.txt, lalu memasangnya kembali dengan uv pip install -r requirements.txt. Namun karena daftar ini juga memuat semua dependensi turunan, proyek yang dikelola uv biasanya lebih rapi bila hanya mencatat paket utama (misalnya fastapi dan sqlmodel) lewat uv add, sehingga pyproject.toml dan uv.lock yang mengurus sisanya.</p>

### 1.5 Install SQLite (command-line tools)

<img width="947" height="425" alt="07_1 5" src="https://github.com/user-attachments/assets/b79ab030-41af-448c-86fc-81d548f49705" />

#### Pembahasan

<p align="justify">Halaman ini adalah SQLite Download Page yang menyediakan unduhan SQLite versi 3.54.1 dalam beberapa kelompok. Ada kode sumber (sqlite-src-3540100.zip sebagai pohon sumber lengkap, serta versi amalgamation dan autoconf yang lebih ringkas untuk dikompilasi), dokumentasi dalam bentuk file HTML statis (sqlite-doc-3540100.zip), pustaka siap pakai untuk Android (sqlite-android-3540100.aar), dan alat command-line untuk Linux x64 (sqlite-tools-linux-x64-3540100.zip) yang berisi shell sqlite3, sqldiff, sqlite3_analyzer, dan sqlite3_rsync. Setiap berkas dilengkapi checksum SHA3-256 untuk memverifikasi keaslian unduhan. Karena kamu memakai Windows, bagian yang relevan ada di sisi bawah halaman, yaitu bagian Precompiled Binaries for Windows (biasanya sqlite-tools-win-x64-...zip untuk shell sqlite3.exe). Namun untuk proyek FastAPI dengan SQLModel, kamu sebenarnya tidak perlu mengunduh apa pun, karena modul sqlite3 sudah bawaan Python dan database SQLite langsung bisa dipakai. Unduhan ini hanya berguna bila ingin membuka dan memeriksa file .db lewat terminal.</p>


Cari lokasi sqlite3.exe untuk memastikan:
```python
where /r . sqlite3.exe
```
<img width="898" height="59" alt="09" src="https://github.com/user-attachments/assets/5362626a-e1a9-44fe-b7f8-483d75e93c9e" />

#### Pembahasan

<p align="justify">Perintah where /r . sqlite3.exe mencari sqlite3.exe secara rekursif dari folder modul dan menemukannya di sqlite-tools-win-x64-3540100\sqlite3.exe, jadi lokasi file ini terkonfirmasi tepat berada di dalam folder modul praktikum. Setelah itu kamu menjalankan lagi perintah set "PATH=%PATH%;%CD%\sqlite-tools-win-x64-3540100" untuk menambahkan folder tersebut ke PATH sesi terminal yang sedang aktif. Seperti sebelumnya, pengaturan ini hanya berlaku sementara sampai terminal ditutup, dan kalau perintah set dijalankan berulang kali, PATH akan berisi entri ganda, yang tidak berbahaya tetapi tidak perlu. Agar permanen dan tidak bergantung pada folder kerja, pertimbangkan memindahkan folder sqlite-tools-win-x64-3540100 ke lokasi tetap seperti C:\sqlite, lalu menambahkannya lewat Environment Variables Windows.</p>


Daftarkan ke PATH
```python
set "PATH=%PATH%;%CD%\sqlite-tools-win-x64-3540100"
sqlite3 --version
```

<img width="466" height="89" alt="08" src="https://github.com/user-attachments/assets/5b576e24-898d-41b9-a61a-bce166dd6ae1" />

#### Pembahasan

<p align="justify">Perintah set "PATH=%PATH%;%CD%\sqlite-tools-win-x64-3540100" menambahkan folder sqlite-tools-win-x64-3540100 di dalam folder modul ke PATH, sehingga sqlite3 bisa dipanggil dari mana saja. Hasil sqlite3 --version menampilkan versi 3.54.1 (build 2026-10-16, 64-bit), yang cocok dengan versi di halaman unduhan sebelumnya, jadi pemasangan alat command-line SQLite berhasil. Perlu diingat bahwa set hanya berlaku untuk jendela terminal yang sedang terbuka, jadi pengaturan ini hilang saat terminal ditutup. Kalau ingin permanen, tambahkan folder itu lewat Environment Variables Windows (sebaiknya dipindah ke lokasi tetap, misalnya C:\sqlite), atau cukup jalankan ulang perintah set di setiap sesi. Setelah ini, kamu bisa membuka database dengan sqlite3 nama.db dan memeriksa tabel lewat perintah .tables atau .schema.</p>

# TUGAS

### 1. Buat satu tabel baru menggunakan SQLite, tabel berbeda dari yang ada pada contoh. Tabel tersebut mempunyai 1 primary key dan setidaknya berisi data dengan tipe INT, CHAR, VARCHAR, BOOLEAN, dan FLOAT.

```python
sqlite3 toko-produk.db
```

Di prompt sqlite>:
```python
CREATE TABLE produk (id INTEGER PRIMARY KEY, kode CHAR(6), nama VARCHAR(50), harga FLOAT, stok INT, tersedia BOOLEAN);
.tables
.schema produk
.quit
```

<img width="730" height="148" alt="10_T1" src="https://github.com/user-attachments/assets/018cac98-14ef-4e05-aee1-74be809ff132" />

#### Pembahasan

<p align="justify">Perintah sqlite3 toko-produk.db membuka database toko-produk.db di shell SQLite 3.54.1, lalu .tables menunjukkan satu tabel bernama produk. Hasil .schema produk memperlihatkan strukturnya: kolom id (INTEGER PRIMARY KEY), kode (CHAR(6)), nama (VARCHAR(50)), harga (FLOAT), stok (INT), dan tersedia (BOOLEAN). Perintah .quit lalu menutup shell dan kamu kembali ke prompt (MODUL). Perlu dicatat, SQLite bersifat fleksibel soal tipe data, jadi panjang CHAR(6) dan VARCHAR(50) tidak benar-benar dipaksakan, dan BOOLEAN disimpan sebagai angka 0 atau 1. Untuk melihat isi tabel, buka lagi databasenya lalu jalankan SELECT * FROM produk;, dan kalau ingin tampilan lebih rapi, aktifkan dulu .headers on dan .mode column.

Buat File Python di Folder MODUL

### Buat File Python di Folder MODUL

```python
notepad isi_data.py
```
Kode py:

```python
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
```


```python
notepad service.py
```
Isi kode service.py:

```python
from typing import List

from fastapi import Depends, FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Produk(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    kode: str
    nama: str
    harga: float
    stok: int
    tersedia: bool


engine = create_engine("sqlite:///toko-produk.db")


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.get("/produk/", response_model=List[Produk])
def read_produk(session: Session = Depends(get_session)):
    statement = select(Produk)
    results = session.exec(statement).all()
    return results
```

Menggecek:
```python
dir *.py
```

<img width="462" height="125" alt="11" src="https://github.com/user-attachments/assets/d2cd028b-a0c5-48a2-bfc6-38e608992cd6" />

#### Pembahasan

<p align="justify">Perintah dir *.py menampilkan dua file Python di folder modul praktikum, yaitu isi_data.py (928 byte) dan service.py (690 byte), keduanya bertanggal 26/11/2026 pukul 10:34. Dari namanya, isi_data.py kemungkinan berisi skrip untuk mengisi data awal ke tabel produk di toko-produk.db, sedangkan service.py biasanya memuat logika layanan atau endpoint yang nanti dijalankan bersama FastAPI. Ukurannya yang kecil menunjukkan isinya masih ringkas, dan karena .venv sudah aktif, kamu bisa menjalankan skrip pengisi data dengan python isi_data.py lalu mengeceknya di SQLite lewat SELECT * FROM produk;. Untuk layanan, jalankan dengan fastapi dev service.py atau uvicorn service:app --reload, asalkan di dalamnya ada objek app.</p>

### 2. Isikan 5 data menggunakan script Python

```python
python isi_data.py
```

<img width="465" height="101" alt="12_T2" src="https://github.com/user-attachments/assets/91844ea1-b152-48c9-8b44-1d3703041da6" />

#### Pembahasan

<p align="justify">Perintah python isi_data.py berjalan sukses dan mencetak kelima baris yang baru disisipkan ke tabel produk, diakhiri pesan "Selesai: 5 data berhasil diisikan." Hasilnya sesuai dugaan sebelumnya: kolom id terisi otomatis dari 1 sampai 5, harga tetap bertipe desimal (misalnya 175000.5 dan 320000.75), dan nilai boolean tersedia tampil sebagai angka, yaitu 1 untuk produk yang tersedia dan 0 untuk Monitor 24 Inci dan Webcam Full HD yang stoknya habis. Karena sebelumnya .venv aktif dan skrip memakai modul sqlite3 bawaan Python, tidak ada paket tambahan yang dibutuhkan. Data ini bisa langsung diperiksa lewat sqlite3 toko-produk.db dengan SELECT * FROM produk;, dan sudah siap dipakai oleh service.py untuk menguji endpoint pembacaan data.</p>

Lihat isi tabel di SQLite:
```python
sqlite3 toko-produk.db
```

```python
.mode table
SELECT * FROM produk;
.quit
```

<img width="466" height="226" alt="13" src="https://github.com/user-attachments/assets/5ba825ff-58de-46ea-85ff-1b759eccd1fa" />

#### Pembahasan

<p align="justify">Perintah sqlite3 toko-produk.db dengan .mode table lalu SELECT * FROM produk; menampilkan isi tabel dalam bentuk tabel rapi, dan hasilnya cocok dengan data yang tadi dimasukkan skrip isi_data.py. Terlihat lima produk dengan id 1 sampai 5: Keyboard Mekanik (450000.0, stok 25), Mouse Wireless (175000.5, stok 40), Monitor 24 Inci (1850000.0, stok 0), Headset Gaming (320000.75, stok 15), dan Webcam Full HD (275000.0, stok 0). Kolom tersedia bernilai 1 untuk tiga produk yang stoknya ada dan 0 untuk monitor dan webcam, sehingga konsisten dengan stoknya. Ini membuktikan data benar-benar tersimpan permanen di file toko-produk.db, bukan hanya tercetak oleh skrip, jadi database siap dipakai oleh service.py untuk menguji endpoint pembacaan data.</p>


### 3. Buat RESTful API endpoint untuk menampilkan semua data yang telah diisikan

Jalankan kode Tunggu sampai muncul Uvicorn running on http://127.0.0.1:8000 dan Application startup complete. Biarkan jendela ini terbuka.

```python
uvicorn service:app --reload
```

<img width="478" height="103" alt="14_T3" src="https://github.com/user-attachments/assets/22d2dcfc-4adf-4cca-acb1-14f1d7e67ed8" />

#### Pembahasan

<p align="justify">Perintah uvicorn service:app --reload berhasil menjalankan layanan FastAPI dari file service.py. Uvicorn aktif di http://127.0.0.1:8000, memantau perubahan file di folder modul lewat WatchFiles (proses reloader 13748 dan proses server 12116), dan log ditutup dengan "Application startup complete", artinya aplikasi siap menerima permintaan. Berkat opsi --reload, setiap kali kamu menyimpan perubahan di service.py, server akan restart otomatis. Sekarang kamu bisa membuka http://127.0.0.1:8000/docs di browser untuk mencoba endpoint lewat Swagger UI, dan tekan CTRL+C di terminal untuk menghentikan server. Karena terminal ini terpakai oleh server, buka jendela terminal baru bila ingin menjalankan perintah lain.</p>

Cek di browser: http://localhost:8000/produk/ (dokumentasi otomatis: http://localhost:8000/docs).

<img width="477" height="134" alt="15" src="https://github.com/user-attachments/assets/8db7d28d-b10b-476f-b960-c7a7c03167fc" />

#### Pembahasan

<p align="justify">Tampilan ini adalah respons JSON dari endpoint layanan FastAPI yang berisi lima produk dari tabel produk, sehingga terbukti service.py berhasil membaca toko-produk.db dan mengirimkannya lewat HTTP. Setiap objek memuat id, kode, nama, harga, stok, dan tersedia, dan nilainya sama dengan hasil SELECT di SQLite sebelumnya. Perbedaannya, kolom tersedia kini tampil sebagai true atau false, bukan 1 dan 0, karena data dikonversi ke tipe boolean saat diubah menjadi JSON. Urutan kuncinya tampak alfabetis (harga, id, tersedia, kode, nama, stok), yang menandakan JSON dibuat dengan sort key, kemungkinan memakai json.dumps(..., sort_keys=True) atau jsonify ala Flask, bukan model Pydantic bawaan FastAPI. Hal ini tidak masalah, tetapi kalau ingin urutan lebih rapi dan dokumentasi otomatis di /docs lebih lengkap, kamu bisa mendefinisikan response_model dengan Pydantic atau SQLModel.</p>

<img width="470" height="229" alt="16" src="https://github.com/user-attachments/assets/73f6e1c6-0c1e-4724-a1f0-27a4055179d8" />

#### Pembahasan

<p align="justify">



### 4. Tampilkan hasil RESTful API endpoint tersebut menggunakan curl.

Buka jendela CMD kedua (tidak perlu venv), lalu:

```python
curl http://localhost:8000/produk/
```

curl langsung memanggil curl.exe bawaan Windows. Hasilnya JSON berisi 5 data:

```python
[{"kode":"PRD001","nama":"Keyboard Mekanik","harga":450000.0,"stok":25,"tersedia":true,"id":1}, ... ]
```

```python
curl -s http://localhost:8000/produk/ | python -m json.tool
```

```python
[
    {
        "harga": 450000.0,
        "id": 1,
        "tersedia": true,
        "kode": "PRD001",
        "nama": "Keyboard Mekanik",
        "stok": 25
    },
    {
        "harga": 175000.5,
        "id": 2,
        "tersedia": true,
        "kode": "PRD002",
        "nama": "Mouse Wireless",
        "stok": 40
    },
    {
        "harga": 1850000.0,
        "id": 3,
        "tersedia": false,
        "kode": "PRD003",
        "nama": "Monitor 24 Inci",
        "stok": 0
    },
    {
        "harga": 320000.75,
        "id": 4,
        "tersedia": true,
        "kode": "PRD004",
        "nama": "Headset Gaming",
        "stok": 15
    },
    {
        "harga": 275000.0,
        "id": 5,
        "tersedia": false,
        "kode": "PRD005",
        "nama": "Webcam Full HD",
        "stok": 0
    }
]
```

#### Pembahasan

<p align="justify">


---
# KESIMPULAN

<p align="justify">


---

# REFERENSI




