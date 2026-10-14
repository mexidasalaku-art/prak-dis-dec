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

<img width="404" height="38" alt="17_Menonaktifkan_Virtual_Environment" src="https://github.com/user-attachments/assets/71f9f342-8206-4f86-94e1-ad98445b8136" />

#### Pembahasan

<p align="justify">proses menonaktifkan virtual environment menggunakan perintah deactivate pada PowerShell. Setelah perintah dijalankan, tanda (workspace-01) menghilang dari terminal, yang menandakan bahwa virtual environment berhasil dinonaktifkan. Terminal kemudian kembali ke kondisi normal tanpa lingkungan virtual yang aktif.</p>

---

### 5. Mengelola Paket

Pasang pandas:

```powershell
uv pip install pandas
```

<img width="357" height="133" alt="18_Instalasi_Pandas_dengan_uv" src="https://github.com/user-attachments/assets/09febd92-0c54-45f5-af75-d54ab198f8e2" />
#### Pembahasan

<p align="justify">proses instalasi library Pandas menggunakan perintah uv pip install pandas melalui PowerShell. Proses instalasi berhasil dengan memasang lima paket, yaitu Pandas versi 3.0.6 beserta dependensinya, seperti NumPy, python-dateutil, six, dan tzdata. Instalasi ini memungkinkan Python digunakan untuk mengolah dan menganalisis data dalam bentuk tabel secara lebih mudah.</p>

Pasang Strawberry GraphQL dan requests (requests dipakai oleh client pada tugas):

```powershell
uv pip install "strawberry-graphql[cli]" requests
```

<img width="496" height="392" alt="19_Instalasi_Strawberry_GraphQL_CLI" src="https://github.com/user-attachments/assets/9e6a855c-238a-4a71-b35f-4c5a3da4cf82" />

#### Pembahasan

<p align="justify">proses instalasi paket strawberry-graphql beserta fitur CLI (Command Line Interface) menggunakan perintah uv pip install "strawberry-graphql[cli]". Proses instalasi berhasil dengan memasang 23 paket yang dibutuhkan, termasuk Strawberry GraphQL, GraphQL Core, Typer, dan Uvicorn. Paket-paket tersebut digunakan untuk membangun API berbasis GraphQL dan menyediakan alat pendukung untuk menjalankan serta mengembangkan aplikasi Python.</p>

Lihat paket terpasang dan simpan ke `requirements.txt`:

```powershell
uv pip list
```

<img width="313" height="461" alt="20_okumentasi_instalasi_library_python" src="https://github.com/user-attachments/assets/93f7859e-a0ac-4daa-9acd-3086e861af65" />

#### Pembahasan

<p align="justify">asil perintah uv pip list yang menampilkan 30 package Python beserta versinya. Package tersebut mendukung pengembangan aplikasi web, pengolahan data, dan komunikasi asynchronous.</p>

```powershell
uv pip freeze > requirements.txt
```

```powershell
type requirements.txt
```
<img width="437" height="434" alt="21_requirements txt" src="https://github.com/user-attachments/assets/cf3e1fc4-ff63-4ac2-97f2-9309709eee3a" />

#### Pembahasan

<p align="justify">File requirements.txt dibuat menggunakan perintah uv pip freeze > requirements.txt untuk menyimpan daftar package Python beserta versinya yang terpasang pada lingkungan aktif. Selanjutnya, perintah cat requirements.txt digunakan untuk menampilkan isi file tersebut di terminal. File ini berfungsi sebagai dokumentasi dependensi proyek sehingga package yang dibutuhkan dapat diinstal kembali menggunakan perintah uv pip install -r requirements.txt.</p>
---

### 6. Membuat Server GraphQL dengan Strawberry

### Mendefinisikan skema

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

<img width="316" height="212" alt="22_schema py" src="https://github.com/user-attachments/assets/45f66278-cc98-4673-b492-cb921b091eaa" />

#### Pembahasan

<p align="justify">Kode di schema.py ini mendefinisikan skema GraphQL sederhana dengan Strawberry: class Book adalah tipe data dengan field title dan author bertipe string, sedangkan class Query memiliki field books yang mengembalikan daftar objek Book, dan dekorator @strawberry.type mengubah class Python biasa menjadi tipe GraphQL. Namun, skema ini baru berisi definisi tipe, sehingga agar bisa dijalankan kamu masih perlu menambahkan resolver yang mengisi data buku serta membuat strawberry.Schema(query=Query).</p>

### Definisikan kumpulan data
---

Jalankan server:

```powershell
def get_books():
    return [
        Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
    ]
```

<img width="344" height="293" alt="23_schema py" src="https://github.com/user-attachments/assets/0f95c539-7331-4547-82eb-2435c9d11f11" />


#### Pembahasan

<p align="justify">Kode ini mendefinisikan skema GraphQL dengan Strawberry: Book adalah tipe dengan field title dan author, get_books() menyediakan data contoh berupa satu buku, dan Query punya field books. Namun books belum terhubung ke get_books(), jadi ubah menjadi books: typing.List[Book] = strawberry.field(resolver=get_books), lalu tambahkan schema = strawberry.Schema(query=Query) di bagian bawah agar skema bisa dijalankan.</p>

### Mendefinisikan Resolver
```powershell
@strawberry.type
class Query:
    books: typing.List[Book] = strawberry.field(resolver=get_books)
```

<img width="474" height="290" alt="24_Mendefinisikan_Resolver" src="https://github.com/user-attachments/assets/3c1b32e4-0238-4bdb-97e8-b5c7b701670f" />


#### Pembahasan

<p align="justify">Kode ini mendefinisikan skema GraphQL dengan Strawberry: Book adalah tipe dengan field title dan author, get_books() menyediakan data contoh, dan field books di Query sudah terhubung ke fungsi itu lewat strawberry.field(resolver=get_books). Yang masih kurang hanya schema = strawberry.Schema(query=Query) di bagian bawah agar skema bisa dijalankan.</p>

### Buat skema dan jalankan
```powershell
schema = strawberry.Schema(query=Query)
```

<img width="500" height="314" alt="25_graphql_schema py" src="https://github.com/user-attachments/assets/0ead68a6-0642-473d-98fb-c7860f80a3e4" />

#### Pembahasan

<p align="justify">Program ini membuat API GraphQL sederhana dengan Strawberry: Book mendefinisikan data buku (title dan author), get_books() menyediakan data contoh, field books di Query mengambil data dari fungsi itu, dan strawberry.Schema(query=Query) menyatukan semuanya agar bisa dijalankan.</p>

```powershell
strawberry dev schema

```

<img width="283" height="101" alt="26_strawberry_server_running" src="https://github.com/user-attachments/assets/81fb78bb-a83e-4c38-a873-e7c7d32a46b6" />
#### Pembahasan

<p align="justify">Server berjalan di http://0.0.0.0:8000/graphql dan skemanya sudah benar: Book punya title dan author (String!, wajib terisi), sedangkan books: [Book!]! berarti daftar buku yang pasti ada. Buka http://localhost:8000/graphql di browser, lalu jalankan { books { title author } } untuk melihat hasilnya.</p>

<img width="814" height="350" alt="27_graphiql_interface" src="https://github.com/user-attachments/assets/b9a28fa8-67d1-4e6d-83dc-6818ad7302b2" />

#### Pembahasan

<p align="justify">Gambar ini menampilkan GraphiQL, alat bawaan Strawberry untuk menulis dan menguji query langsung di browser. Panel kiri adalah editor query, tombol pink di sebelahnya untuk menjalankan query, dan panel kanan akan menampilkan hasilnya. Ketik { books { title author } } di editor, lalu klik tombol run.</p>

### Pada bagian kiri uliskan query berikut:
```powershell
{
  books {
    title
    author
  }
}
```
<img width="814" height="356" alt="28_graphiql_syntax_error" src="https://github.com/user-attachments/assets/b6e18874-5f2c-4caf-8923-4163251ede17" />

#### Pembahasan

<p align="justify">Gambar ini menunjukkan hasil "data": null dengan pesan error Syntax Error: Unexpected <EOF> di baris 26 kolom 2. Artinya query belum lengkap: editor masih berisi teks komentar bawaan (baris berawalan #) tanpa query yang sebenarnya, sehingga GraphQL menemukan akhir file sebelum ada perintah yang valid. Hapus semua isi editor, ketik { books { title author } }, lalu klik tombol run, dan hasilnya akan berisi data “The Great Gatsby”.</p>

<img width="813" height="348" alt="29_graphiql_query_berhasil" src="https://github.com/user-attachments/assets/97c16c61-6fe6-436c-b0fb-bd10189043ff" />

#### Pembahasan

<p align="justify">Gambar ini menunjukkan query berhasil dijalankan di GraphiQL. Di panel kiri, query { books { title author } } meminta field title dan author dari books, dan panel kanan menampilkan hasilnya berupa "data" yang berisi buku “The Great Gatsby” karya F. Scott Fitzgerald, sama persis dengan data dari fungsi get_books(). Tidak ada pesan error lagi, jadi API GraphQL-mu sudah berfungsi dengan benar.</p>



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
