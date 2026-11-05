# Praktikum Minggu MODUL 05 - Fault Tolerance

| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi |
| **Topik** | Fault Tolerance |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 | 
| **Kelas** | IF-1 |

---

#  TUJUAN PRAKTIKUM


---

#  DASAR TEORI

--- 

#  PEMBAHASAN

### Cek Veri Docker

<img width="400" height="106" alt="01_cek-versi-docker" src="https://github.com/user-attachments/assets/1f0e9654-5f8c-48ab-ba2e-1e2d6c92e938" />

#### Pembahasan

<p align="justify">Pada tahap ini dilakukan pengecekan instalasi Docker dan Docker Compose sebelum membangun sistem. Perintah docker --version menampilkan Docker versi 29.9.2, sedangkan docker compose version menampilkan Docker Compose v5.6.1. Keluaran versi tanpa pesan galat menandakan bahwa keduanya sudah terpasang dengan benar dan siap dipakai untuk membangun image serta menjalankan beberapa container, seperti Nginx dan aplikasi BlackSheep, pada tahap berikutnya.</p>

### Folder Kerja

<img width="425" height="146" alt="02" src="https://github.com/user-attachments/assets/a1f610fe-2e22-4cef-a97b-782383d716d2" />

#### Pembahasan

<p align="justify">Pada tahap ini dibuat folder kerja untuk proyek. Perintah mkdir workspace-05 menampilkan pesan bahwa folder tersebut sudah ada, sehingga tidak dibuat ulang. Perintah cd workspace-05 berhasil memindahkan posisi ke dalam folder itu. Saat cd workspace-05 dijalankan lagi, muncul pesan “The system cannot find the path specified” karena tidak ada folder bernama workspace-05 di dalam workspace-05. Perintah cd tanpa argumen lalu menampilkan direktori aktif, yaitu C:\Users\HP\workspace-05, yang memastikan posisi kerja sudah benar untuk langkah berikutnya.</p>


### Daftar Versi python

<img width="951" height="445" alt="03_daftar-versi-python" src="https://github.com/user-attachments/assets/21f5267d-eb6e-4e89-badc-f9c3e1e07fcf" />

#### Pembahasan
Perintah uv python list dijalankan untuk melihat daftar versi Python yang tersedia dan yang sudah terpasang di komputer. Versi dengan lokasi python.exe berwarna biru sudah terpasang, yaitu CPython 3.15.0, 3.14.8, 3.14.4, dan 3.13.0 (di Laragon). Versi bertanda <download available> belum terpasang tetapi bisa diunduh uv, misalnya CPython 3.12 sampai 3.8, PyPy, dan GraalPy. Daftar ini membantu memilih versi yang tepat untuk proyek sebelum membuat virtual environment. Pada tugas ini dipilih CPython 3.14.4.

###
###
###
###
###
###
###
###
###
###
###
###
###
###

**Gambar 2 – Struktur proyek.** 
<p align="justify">Perintah `Get-ChildItem -Force` menampilkan isi folder `blacksheep_lb`, termasuk file tersembunyi. Struktur MVC yang dibuat BlackSheep terdiri dari folder `app` (controller, view, dan konfigurasi aplikasi), `domain` (logika bisnis), dan `tests` (pengujian). File pentingnya adalah `dev.py` sebagai titik masuk server pengembangan, `Dockerfile` untuk membangun image container, `requirements.txt` untuk daftar dependensi, serta `settings.toml` dan `settings.dev.toml` untuk konfigurasi aplikasi. File `.gitignore`, `.dockerignore`, dan `.flake8` dipakai untuk pengelolaan repositori, efisiensi build Docker, dan gaya penulisan kode.</p>

**Gambar 3 – Menjalankan aplikasi secara lokal.** 
<p align="justify">Perintah `python dev.py` menjalankan aplikasi dengan Uvicorn, server ASGI yang cepat, di `http://localhost:44777`. Log menunjukkan server berhasil dimulai ("Application startup complete") dan menerima permintaan `GET /` beserta aset statis seperti `styles/public.css`, `jquery.min.js`, `bootstrap.bundle.min.js`, dan font Font Awesome. Semua permintaan berstatus `200 OK`, jadi aplikasi dan file statisnya berjalan dengan benar.</p>

**Gambar 4 – Tampilan di browser.** 
<p align="justify">Saat `localhost:44777` dibuka, muncul halaman utama BlackSheep dengan menu *Getting Started*, *About*, *Contact*, dan *OpenAPI Docs*. Halaman ini menjelaskan BlackSheep sebagai framework web asinkron untuk aplikasi Python yang berbasis event dan non-blocking, dibangun di atas ASGI dan `asyncio`. Tampilan ini membuktikan bahwa proyek hasil template MVC sudah dapat diakses melalui browser.</p>

**Gambar 5 – Mode auto-reload dan dokumentasi API.** 
<p align="justify">Server dijalankan lagi dengan `StatReload`, yaitu fitur Uvicorn yang memantau perubahan file di direktori proyek. Setiap kali kode diubah, server dimuat ulang otomatis sehingga pengembangan lebih efisien. Aplikasi juga menyediakan dokumentasi API interaktif di `http://localhost:44777/docs/`, yang tersedia karena opsi OpenAPI Documentation diaktifkan saat proyek dibuat.</p>

**Gambar 6 – Server berhasil berjalan.** 
<p align="justify">Gambar ini menunjukkan keluaran `python dev.py` yang lebih ringkas: server dimulai, menunggu startup aplikasi, lalu startup selesai. Ini menandakan tidak ada kesalahan pada konfigurasi maupun dependensi.</p>

**Gambar 7 – Instalasi dependensi proyek.** 
<p align="justify">Perintah `uv pip install -r requirements.txt` memasang paket dari `requirements.txt`, dengan `uv` sebagai pengelola paket yang jauh lebih cepat daripada `pip` biasa. Ada 37 paket yang di-resolve dalam sekitar 1,6 detik dan 13 paket baru terpasang dalam 274 ms. Paket utamanya adalah `uvicorn` (server ASGI), `pydantic` (validasi data), `cryptography` dan `pyjwt` (keamanan dan token), serta `websockets` (komunikasi dua arah). Perubahan versi `markupsafe` dari 3.0.4 ke 3.0.2 menunjukkan penyesuaian versi sesuai berkas dependensi.</p>

**Gambar 8 – Membuat proyek dengan BlackSheep CLI.** 
<p align="justify">Perintah `blacksheep create` meminta beberapa pilihan interaktif. Nama proyeknya `blacksheep_lb`, template `mvc`, dokumentasi OpenAPI diaktifkan, pustaka pembaca konfigurasi `essentials-configuration`, dan format pengaturan `TOML`. Setelah selesai, CLI menampilkan langkah berikutnya: masuk ke folder proyek, memasang `requirements.txt`, lalu menjalankan `python dev.py`.</p>

**Gambar 9 – Memasang BlackSheep dan CLI-nya.** 
<p align="justify">Perintah `uv pip install blacksheep blacksheep-cli` memasang 41 paket, termasuk `blacksheep` 2.6.4 dan `blacksheep-cli` 0.0.5. Paket pendukungnya antara lain `click`, `rich`, dan `questionary` untuk antarmuka CLI, `cookiecutter` dan `jinja2` untuk pembuatan proyek dari template, `h11`, `h2`, dan `httptools` untuk pemrosesan HTTP, serta `essentials-configuration` dan `essentials-openapi` untuk konfigurasi dan dokumentasi API. Setelah langkah ini, perintah `blacksheep create` bisa dipakai.</p>

**Gambar 10 – Memasang framework BlackSheep.** 
<p align="justify">Pada tahap awal, hanya `blacksheep` yang dipasang dan `uv` memasang 14 paket dalam 257 ms. Termasuk di dalamnya dependensi inti seperti `httptools`, `h11`, `h2`, `hpack`, `hyperframe`, `rodi` (dependency injection), dan `guardpost` (autentikasi dan otorisasi). Ini menunjukkan bahwa framework sudah bisa dipakai sebelum CLI ditambahkan.</p>

**Gambar 11 – Mengaktifkan virtual environment.** 
<p align="justify">Perintah `.venv\Scripts\activate` mengaktifkan lingkungan virtual. Awalan `(workspace-05)` pada prompt menandakan lingkungan sudah aktif. Dengan begitu, semua paket dipasang hanya untuk proyek ini dan tidak bentrok dengan instalasi Python global.</p>

**Gambar 12 – Membuat virtual environment.** 
<p align="justify">Perintah `uv venv` membuat folder `.venv` dengan CPython 3.14.4. Virtual environment dipakai agar versi Python dan paket tiap proyek terisolasi, sehingga lebih mudah dikelola dan direproduksi di komputer lain.</p>

**Gambar 13 – Memasang dan mengunci versi Python.** 
<p align="justify">Perintah `uv python install 3.14.4` mengunduh dan memasang Python 3.14.4 (sekitar 20 detik). Perintah `uv python pin 3.14.4` menulis versi tersebut ke file `.python-version`, sehingga `uv` selalu memakai versi yang sama untuk proyek ini.</p>

**Gambar 14 – Melihat daftar versi Python.** 
<p align="justify">Perintah `uv python list` menampilkan versi Python yang sudah terpasang, lengkap dengan lokasinya, dan versi yang masih bisa diunduh, seperti 3.15, 3.13, 3.12, hingga PyPy dan GraalPy. Daftar ini membantu memilih versi yang tepat sebelum membuat virtual environment.</p>

**Gambar 15 – Menyiapkan folder kerja.** 
<p align="justify">Perintah `mkdir workspace-05` menghasilkan pesan bahwa folder sudah ada. Perintah `cd workspace-05` kemudian berpindah ke folder tersebut. Perintah `cd workspace-05` kedua gagal karena path tidak ditemukan (folder sudah berada di dalam `workspace-05`), dan `cd` tanpa argumen mengonfirmasi direktori aktif. Ini hanya kesalahan ringan yang tidak memengaruhi hasil.</p>

**Gambar 16 – Memeriksa Docker.** 
<p align="justify">Perintah `docker --version` menampilkan Docker 29.9.2 dan `docker compose version` menampilkan Compose v5.6.1. Keduanya wajib terpasang karena seluruh layanan dijalankan sebagai container dan didefinisikan lewat Docker Compose.</p>

**Gambar 17 – Hasil akhir: container berjalan.** 
<p align="justify">Setelah build selesai (sekitar 241 detik), tampil ringkasan `up 6/6`: image `workspace-05-bs_app` dan `workspace-05-nginx` berhasil dibuat, jaringan `workspace-05_default` dibuat, dan tiga container berstatus *Started*, yaitu `workspace-05-bs_app-1`, `workspace-05-bs_app-2`, dan `nginx`. Nginx berfungsi sebagai load balancer (reverse proxy) yang meneruskan permintaan pengguna ke dua instance aplikasi BlackSheep secara bergantian. Dengan cara ini beban terbagi rata, dan jika satu instance gagal, instance lain masih bisa melayani permintaan. Hal ini menunjukkan prinsip dasar sistem terdistribusi, yaitu skalabilitas, ketersediaan tinggi, dan toleransi kesalahan.</p>


---

# KESIMPULAN


---
# REFERENSI


