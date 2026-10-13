# Praktikum Minggu MODUL 02 - Komunikasi Antar Proses pada Sistem Terdistribusi

| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi |
| **Topik** | Komunikasi Antar Proses pada Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 |
| **Kelas** | IF-1 |

---


---

#  Tujuan Praktikum

1. Mempelajari apa itu proses dan bagaimana sistem operasi mengatur proses-proses yang berjalan dalam satu komputer.
2. Melihat proses apa saja yang sedang aktif di Windows dengan memanfaatkan Task Manager.
3. Mencoba membuka sebuah aplikasi, lalu menghentikan dan menjalankan kembali prosesnya lewat perintah di CMD.
4. Mempraktikkan cara dua proses saling bertukar data pada sistem terdistribusi, yaitu dengan membangun server GraphQL berbasis Python (Strawberry) dan sebuah client yang meminta data darinya.
---

#  Dasar Teori

## Proses

Proses adalah hasil eksekusi sebuah program. Proses dikelola oleh sistem operasi dan terdiri atas kode executable, data, resources, serta informasi state (stack dan heap). Setiap aplikasi yang dijalankan menjadi sebuah proses.

## Proses pada Satu Node

Pada satu node, semua proses dikendalikan oleh sistem operasi: eksekusi, alokasi resources, pengelolaan, hingga komunikasi antar proses. Semua proses memakai clock yang sama dan dapat memakai shared memory, sehingga tidak perlu sinkronisasi antar node.

## Komunikasi Antar Proses pada Sistem Terdistribusi

Pada sistem terdistribusi, setiap node punya clock dan memori sendiri sehingga shared memory tidak bisa dipakai. Karena itu dibutuhkan mekanisme khusus untuk komunikasi antar proses di node berbeda. Salah satunya adalah GraphQL: server melayani query dari client sesuai spesifikasi GraphQL. Pada praktikum ini server dibuat dengan Python dan paket Strawberry (https://strawberry.rocks/).

## Perintah Windows yang Digunakan

| Perintah                          | Fungsi                                         |
| --------------------------------- | ---------------------------------------------- |
| `tasklist`                        | Menampilkan daftar proses yang sedang berjalan |
| `tasklist \| findstr /i "nama"`   | Mencari proses tertentu berdasarkan nama       |
| `taskkill /IM nama_proses.exe /F` | Mematikan proses secara paksa                  |
| `start "" notepad`                | Menjalankan kembali aplikasi                   |

---

#  PEMBAHASAN PRAKTIKUM

## PRAKTIK 1 - PROSES PADA SATU NODE

### 1. Tampilkan berbagai proses pada Windows

Buka Task Manager (`Ctrl + Shift + Esc`).

<img width="921" height="469" alt="image" src="https://github.com/user-attachments/assets/6849da7d-806a-4e91-b5cd-b11f35c90a3c" />


#### Pembahasan

<p align="justify">Task Manager adalah aplikasi bawaan Windows untuk melihat proses yang sedang berjalan beserta PID, CPU, dan memori yang dipakainya. Dari sini terlihat bahwa setiap aplikasi yang berjalan adalah sebuah proses yang dikelola sistem operasi secara otomatis.</p>

---

### 2. Jalankan aplikasi dan perlihatkan prosesnya

Contoh: menjalankan word.

<img width="951" height="500" alt="02_proses_word" src="https://github.com/user-attachments/assets/0aa554fb-184d-42f4-9621-a24c8701e735" />


Proses yang muncul dapat dilihat di Task Manager:

<img width="356" height="141" alt="03_detail_word" src="https://github.com/user-attachments/assets/bbdd66a6-0b98-4319-b5df-ca711676c5b5" />


#### Pembahasan

<p align="justify">Setelah Word dibuka, muncul proses WINWORD.EXE. Artinya file program yang semula hanya tersimpan di disk kini dieksekusi sistem operasi menjadi proses. Pada tab Details terlihat PID dan status proses sehingga dapat dibedakan dari proses lain.</p>

---

### 3. Mematikan dan me-restart proses

#### Mematikan proses lewat Task Manager

Klik kanan proses `WINWORD.EXE`, lalu pilih **End task**.

<img width="772" height="361" alt="04_and_task" src="https://github.com/user-attachments/assets/c91a2b85-02cc-46a4-a374-3b40cdfe8990" />

#### Pembahasan

<p align="justify">End task menghentikan proses di level sistem operasi, bukan sekadar menutup jendela aplikasi.</p>

---

#### Melihat daftar proses lewat CMD

```powershell
tasklist
```

<img width="543" height="156" alt="05_tasklist" src="https://github.com/user-attachments/assets/b3a8f825-effc-43a3-bce0-ee5ea0ab79d5" />

#### Pembahasan

<p align="justify">Perintah <code>tasklist</code> menampilkan daftar proses dalam bentuk teks di terminal, setara dengan yang ada di Task Manager.</p>

---

#### Mencari proses tertentu

```powershell
tasklist | findstr /i winword
```

<img width="475" height="51" alt="06_tasklist_winword" src="https://github.com/user-attachments/assets/b96f1157-03d4-43e5-8138-50a3a295f515" />

#### Pembahasan

<p align="justify">Hasil <code>tasklist</code> disaring dengan <code>findstr</code> agar hanya proses yang dicari yang tampil. Opsi <code>/i</code> membuat pencarian tidak membedakan huruf besar dan kecil.</p>

---

#### Mematikan proses lewat CMD

```powershell
taskkill /IM WINWORD.EXE /F
```

<img width="518" height="47" alt="07_Menutup_Proses_Microsoft_Word" src="https://github.com/user-attachments/assets/2e93456e-c5ee-4fb8-954a-e0f3cb7ae707" />

#### Pembahasan

<p align="justify"><code>/IM</code> Menunjuk proses berdasarkan nama file executable, sedangkan /F memaksa proses berhenti meskipun tidak merespons. Setelah dijalankan, aplikasi Microsoft Word tertutup.</p>

---

#### Memastikan proses sudah berhenti

```powershell
tasklist | findstr /i winword
```

<img width="392" height="34" alt="08_Mengecek_Proses_Winword" src="https://github.com/user-attachments/assets/d3dea140-c79d-4207-ab93-ff00882ab6b6" />

#### Pembahasan

<p align="justify">Tidak terdapat hasil yang ditampilkan, sehingga dapat disimpulkan bahwa proses WINWORD.EXE sudah tidak berjalan pada sistem.</p>

---

#### Me-restart proses

```powershell
start "" winword
```

<img width="301" height="52" alt="09_Menjalankan_Microsoft_Winword" src="https://github.com/user-attachments/assets/c8291a6f-31c9-4297-8248-2079bdce4181" />

#### Pembahasan

<p align="justify">Perintah start menganggap argumen pertama sebagai judul jendela, sehingga tanda "" diperlukan agar winword dibaca sebagai nama program. Setelah perintah dijalankan, proses WINWORD.EXE kembali berjalan dengan PID yang baru.</p>

---

## PRAKTIK 2 - KOMUNIKASI ANTAR PROSES PADA SISTEM TERDISTRIBUSI

### 1. Instalasi uv

Petunjuk lengkap: https://docs.astral.sh/uv/getting-started/installation/

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Pastikan folder instalasi (`C:\Users\HP\.local\bin`) ada di PATH, lalu cek:

```powershell
uv --version
```

<img width="695" height="212" alt="10_Instalasi_uv" src="https://github.com/user-attachments/assets/5e84816c-b091-4586-b8a4-e7ba6000e74a" />

#### Pembahasan

<p align="justify">Gambar tersebut menunjukkan proses instalasi uv versi 0.13.0 melalui PowerShell. Instalasi berhasil dilakukan, dan perintah uv --version digunakan untuk memastikan bahwa uv telah terpasang dan dapat dijalankan dengan baik.</p>

---
```powershell
PS C:\Users\HP> uv
An extremely fast Python package manager.

Usage: uv.exe [OPTIONS] <COMMAND>

Commands:
  auth       Manage authentication
  run        Run a command or script
  init       Create a new project
  add        Add dependencies to the project
  remove     Remove dependencies from the project
  version    Read or update the project's version
  sync       Update the project's environment
  lock       Update the project's lockfile
  export     Export the project's lockfile to an alternate format
  tree       Display the project's dependency tree
  format     Format Python code in the project
  check      Run checks on the project
  audit      Audit the project's dependencies
  tool       Run and install commands provided by Python packages
  python     Manage Python versions and installations
  pip        Manage Python packages with a pip-compatible interface
  venv       Create a virtual environment
  build      Build Python packages into source distributions and wheels
  publish    Upload distributions to an index
  workspace  Inspect uv workspaces
  cache      Manage uv's cache
  self       Manage the uv executable
  help       Display documentation for a command

Cache options:
  -n, --no-cache               Avoid reading from or writing to the cache, instead using a temporary directory for the duration of
                               the operation [env: UV_NO_CACHE=]
      --cache-dir <CACHE_DIR>  Path to the cache directory [env: UV_CACHE_DIR=]

Python options:
      --managed-python       Require use of uv-managed Python versions [env: UV_MANAGED_PYTHON=]
      --no-managed-python    Disable use of uv-managed Python versions [env: UV_NO_MANAGED_PYTHON=]
      --no-python-downloads  Disable automatic downloads of Python. [env: "UV_PYTHON_DOWNLOADS=never"]

Global options:
  -q, --quiet...                                   Use quiet output
  -v, --verbose...                                 Use verbose output
      --color <COLOR_CHOICE>                       Control the use of color in output [possible values: auto, always, never]
      --system-certs                               Whether to load TLS certificates from the platform's native certificate store
                                                   [env: UV_SYSTEM_CERTS=]
      --offline                                    Disable network access [env: UV_OFFLINE=]
      --allow-insecure-host <ALLOW_INSECURE_HOST>  Allow insecure connections to a host [env: UV_INSECURE_HOST=]
      --no-progress                                Hide all progress outputs [env: UV_NO_PROGRESS=]
      --directory <DIRECTORY>                      Change to the given directory prior to running the command [env: UV_WORKING_DIR=]
      --project <PROJECT>                          Discover a project in the given directory [env: UV_PROJECT=]
      --config-file <CONFIG_FILE>                  The path to a `uv.toml` file to use for configuration [env: UV_CONFIG_FILE=]
      --no-config                                  Avoid discovering configuration files (`pyproject.toml`, `uv.toml`) [env:
                                                   UV_NO_CONFIG=]
  -h, --help                                       Display the concise help for this command
  -V, --version                                    Display the uv version

Use `uv help` for more details.
PS C:\Users\HP>
```
#### Pembahasan

<p align="justify">uv berhasil dijalankan melalui PowerShell. Tampilan yang muncul berisi daftar perintah dan fungsi uv, seperti init untuk membuat proyek baru, run untuk menjalankan program, dan venv untuk membuat lingkungan virtual Python. Hal ini menandakan bahwa uv telah terpasang dan siap digunakan.</p>

### 2. Update uv

```powershell
uv self update
```

<img width="497" height="65" alt="11_Verifikasi_Update_uv" src="https://github.com/user-attachments/assets/07f6249d-a34a-4937-8a1b-78c67ec4c599" />

#### Pembahasan

<p align="justify">proses pemeriksaan pembaruan aplikasi uv menggunakan perintah uv self update melalui Windows PowerShell. Perintah ini digunakan untuk memeriksa apakah tersedia versi uv yang lebih baru. Setelah proses pemeriksaan selesai, muncul pesan bahwa uv versi 0.13.0 sudah merupakan versi terbaru. Dengan demikian, aplikasi uv tidak memerlukan pembaruan lebih lanjut dan siap digunakan untuk mengelola paket Python, membuat lingkungan virtual, serta menjalankan proyek Python.</p>

---

### 3. Membuat Workspace

```powershell
cd workspace-01
mkdir workspace-02
uv python list
```

<img width="446" height="156" alt="12_Membuat_Folder_Workspace_Baru" src="https://github.com/user-attachments/assets/3c8fb983-6a2c-46e4-aff4-48f4cdabc154" />

#### Pembahasan
<p align="justify">proses pembuatan folder baru bernama workspace-02 di dalam direktori workspace-01 menggunakan perintah mkdir pada PowerShell. Perintah cd workspace-01 digunakan untuk masuk ke direktori tersebut, sedangkan mkdir workspace-02 digunakan untuk membuat folder baru sebagai tempat menyimpan file atau proyek.</p>

<img width="953" height="362" alt="13_Daftar_Versi_Python_dengan_uv" src="https://github.com/user-attachments/assets/011fb0ac-42ac-4ed6-8ff1-460a41e96b9d" />

#### Pembahasan

<p align="justify">penggunaan perintah uv python list untuk menampilkan berbagai versi Python yang tersedia. Daftar tersebut mencakup versi yang dapat diunduh maupun versi yang sudah terpasang di komputer. Perintah ini membantu pengguna mengetahui pilihan versi Python yang dapat digunakan untuk menjalankan proyek sesuai kebutuhan.</p>

<img width="626" height="61" alt="14_Konfigurasi_Versi_Python_uv" src="https://github.com/user-attachments/assets/fbe30200-f347-4a7b-892b-b6d4fbb730df" />

#### Pembahasan
<p align="justify">proses pengaturan versi Python menggunakan perintah uv python pin pada PowerShell. Perintah ini digunakan untuk menentukan interpreter Python yang akan digunakan dalam proyek dengan menyimpan lokasinya ke file .python-version. Selanjutnya, perintah cat .python-version digunakan untuk menampilkan isi file tersebut. Hasilnya menunjukkan lokasi Python di C:\Users\HP\.local\bin\python3.14.exe, sehingga konfigurasi versi Python berhasil disimpan.</p>

---

### 4. Membuat Environment

```powershell
uv venv
.\.venv\Scripts\activate
where python
```

<img width="842" height="85" alt="15_Membuat_Virtual_Environment_Python" src="https://github.com/user-attachments/assets/bb28a0ef-c35e-4e40-8124-7a1277b1c951" />

#### Pembahasan

<p align="justify">proses pembuatan lingkungan virtual Python menggunakan perintah uv venv. Lingkungan virtual dibuat pada folder .venv dengan menggunakan interpreter CPython versi 3.14.8. Karena folder .venv sudah tersedia, sistem meminta konfirmasi untuk menggantinya. Pengguna memilih yes untuk melanjutkan proses penggantian lingkungan virtual yang sudah ada.</p>

<img width="577" height="61" alt="16_Aktivasi_Virtual_Environment_Python" src="https://github.com/user-attachments/assets/4ec7e1d9-3e0e-4396-881c-8901e26d0774" />

#### Pembahasan
<p align="justify">proses aktivasi virtual environment menggunakan perintah .\.venv\Scripts\Activate pada PowerShell. Setelah aktivasi berhasil, muncul tanda (workspace-01) pada terminal. Selanjutnya, perintah python dijalankan untuk membuka interpreter Python versi 3.14.8. Hal ini menunjukkan bahwa lingkungan virtual telah aktif dan Python siap digunakan untuk menjalankan kode program.</p>

Untuk keluar dari environment:

```powershell
deactivate
```

<img src="images/18_Deactivate.png" width="700">

#### Pembahasan

<p align="justify"><code>uv venv</code> membuat environment terisolasi di folder <code>.venv</code>. Setelah diaktifkan, prompt diawali nama environment dan <code>where python</code> menunjuk ke <code>.venv\Scripts\python.exe</code>, artinya semua paket yang dipasang masuk ke environment ini. <code>deactivate</code> mengembalikan terminal ke Python sistem.</p>

<img width="404" height="38" alt="17_Menonaktifkan_Virtual_Environment" src="https://github.com/user-attachments/assets/71f9f342-8206-4f86-94e1-ad98445b8136" />

#### Pembahasan

<p align="justify">proses menonaktifkan virtual environment menggunakan perintah deactivate pada PowerShell. Setelah perintah dijalankan, tanda (workspace-01) menghilang dari terminal, yang menandakan bahwa virtual environment berhasil dinonaktifkan. Terminal kemudian kembali ke kondisi normal tanpa lingkungan virtual yang aktif.</p>

---

### 5. Mengelola Paket

Pasang pandas:

```powershell
uv pip install pandas
```

<img src="images/19_Install_Pandas.png" width="700">

Pasang Strawberry GraphQL dan requests (requests dipakai oleh client pada tugas):

```powershell
uv pip install "strawberry-graphql[cli]" requests
```

<img src="images/20_Install_Strawberry.png" width="700">

Lihat paket terpasang dan simpan ke `requirements.txt`:

```powershell
uv pip list
uv pip freeze > requirements.txt
type requirements.txt
```

<img src="images/21_Daftar_Paket.png" width="700">

#### Pembahasan

<p align="justify"><code>uv pip install</code> mengunduh paket beserta dependensinya ke environment aktif. Tambahan <code>[cli]</code> pada Strawberry memasang perintah <code>strawberry</code> untuk menjalankan server. <code>uv pip freeze</code> menyimpan daftar paket berikut versinya ke <code>requirements.txt</code> sehingga lingkungan yang sama dapat dipasang ulang di komputer lain.</p>

---

### 6. Membuat Server GraphQL dengan Strawberry

Buat file `schema.py`. Urutan penulisan penting: `Book` dan `get_books` harus didefinisikan sebelum `Query` yang memakainya.

```python
import typing
import strawberry


@strawberry.type
class Book:
    title: str
    author: str


def get_books():
    return [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
    ]


@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)


schema = strawberry.Schema(query=Query)
```

<img src="images/22_File_schema.png" width="700">

#### Pembahasan

<p align="justify">Skema terdiri dari empat bagian. <code>Book</code> adalah tipe data dengan field <code>title</code> dan <code>author</code>. <code>get_books</code> menyediakan data. <code>Query</code> mendefinisikan field <code>books</code> yang dihubungkan ke <code>get_books</code> lewat resolver. Terakhir, <code>strawberry.Schema(query=Query)</code> merangkai semuanya menjadi skema yang dilayani server.</p>

---

Jalankan server:

```powershell
strawberry dev schema
```

<img src="images/23_Jalankan_Server.png" width="700">

Output: `Running strawberry on http://0.0.0.0:8000/graphql` (dapat diakses lewat `http://localhost:8000/graphql`).

<img src="images/24_Tampilan_GraphQL.png" width="700">

#### Pembahasan

<p align="justify">Server berjalan di port 8000. Saat alamatnya dibuka di browser, muncul antarmuka GraphQL bawaan Strawberry: sisi kiri untuk menulis query dan sisi kanan untuk melihat hasil. Alamat <code>0.0.0.0</code>, <code>localhost</code>, dan <code>127.0.0.1</code> merujuk ke komputer yang sama.</p>

---

Tulis query berikut di sisi kiri lalu klik tombol **Run**:

```graphql
{
  books {
    title
    author
  }
}
```

<img src="images/25_Query_GraphQL.png" width="700">

<img src="images/26_Output_Query.png" width="700">

Untuk mematikan server tekan `Ctrl + C` pada terminal tempat server berjalan.

#### Pembahasan

<p align="justify">Query meminta field <code>books</code> beserta <code>title</code> dan <code>author</code>. Server menjalankan resolver <code>get_books</code> dan mengembalikan data The Great Gatsby karya F. Scott Fitzgerald. Alurnya: client mengirim query, server menjalankan resolver, hasil dikembalikan ke client.</p>

---

#  PEMBAHASAN TUGAS

### 1. Buat file `client.py`

<img src="images/27_Tugas_File_client.png" width="700">

### 2. Isi file dengan kode berikut

```python
import requests

url = "http://localhost:8000/graphql"

query = """
{
  books {
    title
    author
  }
}
"""

try:
  response = requests.post(url, json={"query": query})

  if response.status_code == 200:
    data = response.json()
    books = data.get("data", {}).get("books", [])

    print("=== DATA DARI GRAPHQL SERVER ===")
    for book in books:
      print(f"- Judul : {book.get('title')}")
      print(f"- Penulis: {book.get('author')}")
    print("--------------------------------")
  else:
    print(f"Gagal terhubung. Status code: {response.status_code}")

except Exception as e:
  print(f"Terjadi kesalahan: {e}")
```

<img src="images/28_Tugas_Isi_client.png" width="700">

#### Pembahasan

<p align="justify">Client memakai library <code>requests</code> untuk mengirim HTTP POST berisi query ke server. Jika status code 200, data buku diambil dari <code>data.books</code> pada response JSON dan ditampilkan satu per satu. Jika gagal, pesan error ditampilkan.</p>

---

### 3. Jalankan `client.py`

Biarkan server tetap berjalan di satu terminal, lalu buka terminal kedua, aktifkan environment, dan jalankan:

```powershell
python client.py
```

<img src="images/29_Output_client.png" width="700">

#### Pembahasan

<p align="justify">Client menampilkan judul dan penulis buku yang diambil dari server. Ini menunjukkan dua proses terpisah, client dan server, berhasil berkomunikasi dan bertukar data melalui GraphQL.</p>

---

#  Kesimpulan

1. Pada satu node, proses dikelola sepenuhnya oleh sistem operasi dan dapat dilihat dengan `tasklist`, dimatikan dengan `taskkill`, dan dijalankan kembali dengan `start`.
2. Pada sistem terdistribusi, komunikasi antar proses memerlukan mekanisme khusus karena clock berbeda dan tidak ada shared memory. GraphQL adalah salah satu caranya.
3. Server GraphQL berhasil dibuat dengan Python dan Strawberry, serta dapat diakses di `http://localhost:8000/graphql`.
4. `client.py` berhasil mengirim query ke server dan menampilkan data buku yang diminta.

---

## Referensi

- https://strawberry.rocks/docs
- https://docs.astral.sh/uv/getting-started/installation/
- https://github.com/NEO-X-School/notes/blob/main/uv/00.mdc
