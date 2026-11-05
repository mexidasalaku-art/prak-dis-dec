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
# Pembahasan


**Gambar 1 – Build dan menjalankan container dengan scaling.** 
Perintah `docker compose up --build -d --scale bs_app=2` membangun image dari `Dockerfile` lalu menjalankan seluruh layanan di latar belakang (`-d`). Proses build menarik image dasar `nginx:latest` dan `python:3.13.1-slim`, lalu mengekstrak setiap layer. Pada tahap `server_builder`, sistem memasang paket pendukung lewat `apt-get`, yang memakan waktu paling lama (sekitar 120 detik). Opsi `--scale bs_app=2` membuat dua replika layanan aplikasi sekaligus. Dua replika inilah yang nantinya menerima pembagian beban dari Nginx.<

**Gambar 2 – Struktur proyek.** 
Perintah `Get-ChildItem -Force` menampilkan isi folder `blacksheep_lb`, termasuk file tersembunyi. Struktur MVC yang dibuat BlackSheep terdiri dari folder `app` (controller, view, dan konfigurasi aplikasi), `domain` (logika bisnis), dan `tests` (pengujian). File pentingnya adalah `dev.py` sebagai titik masuk server pengembangan, `Dockerfile` untuk membangun image container, `requirements.txt` untuk daftar dependensi, serta `settings.toml` dan `settings.dev.toml` untuk konfigurasi aplikasi. File `.gitignore`, `.dockerignore`, dan `.flake8` dipakai untuk pengelolaan repositori, efisiensi build Docker, dan gaya penulisan kode.

**Gambar 3 – Menjalankan aplikasi secara lokal.** 
Perintah `python dev.py` menjalankan aplikasi dengan Uvicorn, server ASGI yang cepat, di `http://localhost:44777`. Log menunjukkan server berhasil dimulai ("Application startup complete") dan menerima permintaan `GET /` beserta aset statis seperti `styles/public.css`, `jquery.min.js`, `bootstrap.bundle.min.js`, dan font Font Awesome. Semua permintaan berstatus `200 OK`, jadi aplikasi dan file statisnya berjalan dengan benar.

**Gambar 4 – Tampilan di browser.** 
Saat `localhost:44777` dibuka, muncul halaman utama BlackSheep dengan menu *Getting Started*, *About*, *Contact*, dan *OpenAPI Docs*. Halaman ini menjelaskan BlackSheep sebagai framework web asinkron untuk aplikasi Python yang berbasis event dan non-blocking, dibangun di atas ASGI dan `asyncio`. Tampilan ini membuktikan bahwa proyek hasil template MVC sudah dapat diakses melalui browser.

**Gambar 5 – Mode auto-reload dan dokumentasi API.** Server dijalankan lagi dengan `StatReload`, yaitu fitur Uvicorn yang memantau perubahan file di direktori proyek. Setiap kali kode diubah, server dimuat ulang otomatis sehingga pengembangan lebih efisien. Aplikasi juga menyediakan dokumentasi API interaktif di `http://localhost:44777/docs/`, yang tersedia karena opsi OpenAPI Documentation diaktifkan saat proyek dibuat.

**Gambar 6 – Server berhasil berjalan.** Gambar ini menunjukkan keluaran `python dev.py` yang lebih ringkas: server dimulai, menunggu startup aplikasi, lalu startup selesai. Ini menandakan tidak ada kesalahan pada konfigurasi maupun dependensi.

**Gambar 7 – Instalasi dependensi proyek.** Perintah `uv pip install -r requirements.txt` memasang paket dari `requirements.txt`, dengan `uv` sebagai pengelola paket yang jauh lebih cepat daripada `pip` biasa. Ada 37 paket yang di-resolve dalam sekitar 1,6 detik dan 13 paket baru terpasang dalam 274 ms. Paket utamanya adalah `uvicorn` (server ASGI), `pydantic` (validasi data), `cryptography` dan `pyjwt` (keamanan dan token), serta `websockets` (komunikasi dua arah). Perubahan versi `markupsafe` dari 3.0.4 ke 3.0.2 menunjukkan penyesuaian versi sesuai berkas dependensi.

**Gambar 8 – Membuat proyek dengan BlackSheep CLI.** Perintah `blacksheep create` meminta beberapa pilihan interaktif. Nama proyeknya `blacksheep_lb`, template `mvc`, dokumentasi OpenAPI diaktifkan, pustaka pembaca konfigurasi `essentials-configuration`, dan format pengaturan `TOML`. Setelah selesai, CLI menampilkan langkah berikutnya: masuk ke folder proyek, memasang `requirements.txt`, lalu menjalankan `python dev.py`.

**Gambar 9 – Memasang BlackSheep dan CLI-nya.** Perintah `uv pip install blacksheep blacksheep-cli` memasang 41 paket, termasuk `blacksheep` 2.6.4 dan `blacksheep-cli` 0.0.5. Paket pendukungnya antara lain `click`, `rich`, dan `questionary` untuk antarmuka CLI, `cookiecutter` dan `jinja2` untuk pembuatan proyek dari template, `h11`, `h2`, dan `httptools` untuk pemrosesan HTTP, serta `essentials-configuration` dan `essentials-openapi` untuk konfigurasi dan dokumentasi API. Setelah langkah ini, perintah `blacksheep create` bisa dipakai.

**Gambar 10 – Memasang framework BlackSheep.** Pada tahap awal, hanya `blacksheep` yang dipasang dan `uv` memasang 14 paket dalam 257 ms. Termasuk di dalamnya dependensi inti seperti `httptools`, `h11`, `h2`, `hpack`, `hyperframe`, `rodi` (dependency injection), dan `guardpost` (autentikasi dan otorisasi). Ini menunjukkan bahwa framework sudah bisa dipakai sebelum CLI ditambahkan.

**Gambar 11 – Mengaktifkan virtual environment.** Perintah `.venv\Scripts\activate` mengaktifkan lingkungan virtual. Awalan `(workspace-05)` pada prompt menandakan lingkungan sudah aktif. Dengan begitu, semua paket dipasang hanya untuk proyek ini dan tidak bentrok dengan instalasi Python global.

**Gambar 12 – Membuat virtual environment.** Perintah `uv venv` membuat folder `.venv` dengan CPython 3.14.4. Virtual environment dipakai agar versi Python dan paket tiap proyek terisolasi, sehingga lebih mudah dikelola dan direproduksi di komputer lain.

**Gambar 13 – Memasang dan mengunci versi Python.** Perintah `uv python install 3.14.4` mengunduh dan memasang Python 3.14.4 (sekitar 20 detik). Perintah `uv python pin 3.14.4` menulis versi tersebut ke file `.python-version`, sehingga `uv` selalu memakai versi yang sama untuk proyek ini.

**Gambar 14 – Melihat daftar versi Python.** Perintah `uv python list` menampilkan versi Python yang sudah terpasang, lengkap dengan lokasinya, dan versi yang masih bisa diunduh, seperti 3.15, 3.13, 3.12, hingga PyPy dan GraalPy. Daftar ini membantu memilih versi yang tepat sebelum membuat virtual environment.

**Gambar 15 – Menyiapkan folder kerja.** Perintah `mkdir workspace-05` menghasilkan pesan bahwa folder sudah ada. Perintah `cd workspace-05` kemudian berpindah ke folder tersebut. Perintah `cd workspace-05` kedua gagal karena path tidak ditemukan (folder sudah berada di dalam `workspace-05`), dan `cd` tanpa argumen mengonfirmasi direktori aktif. Ini hanya kesalahan ringan yang tidak memengaruhi hasil.

**Gambar 16 – Memeriksa Docker.** Perintah `docker --version` menampilkan Docker 29.9.2 dan `docker compose version` menampilkan Compose v5.6.1. Keduanya wajib terpasang karena seluruh layanan dijalankan sebagai container dan didefinisikan lewat Docker Compose.

**Gambar 17 – Hasil akhir: container berjalan.** Setelah build selesai (sekitar 241 detik), tampil ringkasan `up 6/6`: image `workspace-05-bs_app` dan `workspace-05-nginx` berhasil dibuat, jaringan `workspace-05_default` dibuat, dan tiga container berstatus *Started*, yaitu `workspace-05-bs_app-1`, `workspace-05-bs_app-2`, dan `nginx`. Nginx berfungsi sebagai load balancer (reverse proxy) yang meneruskan permintaan pengguna ke dua instance aplikasi BlackSheep secara bergantian. Dengan cara ini beban terbagi rata, dan jika satu instance gagal, instance lain masih bisa melayani permintaan. Hal ini menunjukkan prinsip dasar sistem terdistribusi, yaitu skalabilitas, ketersediaan tinggi, dan toleransi kesalahan.

## Kesimpulan

Praktik ini menunjukkan alur lengkap pengembangan aplikasi web asinkron dengan BlackSheep. Alur itu dimulai dari menyiapkan lingkungan Python (`uv`, virtual environment, dan versi Python), membuat proyek lewat CLI, dan menguji secara lokal. Setelah itu aplikasi dikemas dalam Docker dan didistribusikan ke dua instance dengan Nginx sebagai load balancer. Hasilnya adalah sistem yang lebih skalabel dan andal dibandingkan menjalankan satu server tunggal.


---


#  PEMBAHASAN

---

# KESIMPULAN


---
# REFERENSI


