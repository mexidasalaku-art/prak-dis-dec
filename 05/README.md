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

- Memahami fault tolerance, yaitu kemampuan sistem untuk terus melayani permintaan meskipun sebagian komponennya mengalami kegagalan.
- Menjalankan aplikasi BlackSheep dalam beberapa instance sekaligus dengan Docker Compose.
- Mengonfigurasi nginx agar meneruskan request ke instance-instance aplikasi.
- Membuktikan bahwa request terbagi ke beberapa instance dengan melihat log setiap container.
- Mengenali kegagalan koneksi dan menanganinya dengan heartbeat, retry, dan circuit breaker.

---

#  DASAR TEORI

<p align="justify">Sistem terdistribusi tersusun dari banyak komponen, dan setiap komponen bisa berhenti berfungsi sewaktu-waktu. Proses bisa mati, jaringan bisa terputus, atau host bisa kehabisan sumber daya. Fault tolerance adalah kemampuan sistem untuk tetap melayani permintaan saat kejadian seperti itu muncul. Salah satu caranya adalah menjalankan beberapa salinan dari layanan yang sama, sehingga tidak ada satu titik pun yang bila gagal akan menghentikan seluruh layanan. Selama masih ada satu salinan yang hidup, pengguna seharusnya tidak merasakan adanya gangguan.</p>

<p align="justify">Ketika ada beberapa salinan aplikasi, dibutuhkan pihak yang menentukan salinan mana yang menerima tiap request. nginx dapat berperan sebagai reverse proxy: klien cukup menghubungi satu alamat, lalu nginx meneruskan request ke salah satu server dalam grup upstream. Metode paling sederhana adalah round-robin, yaitu request dibagikan secara bergiliran menurut urutan server. Docker Compose menyediakan opsi scale untuk membuat banyak replika, dan nama service seperti bs_app berfungsi sebagai alamat yang diterjemahkan ke seluruh replika tersebut. Dengan begitu, konfigurasi nginx tidak perlu menuliskan alamat IP satu per satu.</p>

<p align="justify">Load balancer hanya bertugas membagi trafik, sehingga kondisi tiap komponen tetap perlu dipantau. Pada protokol heartbeat, sebuah komponen dianggap sehat selama ia masih mengirim sinyal dalam rentang waktu tertentu. Jika sinyal tidak diterima hingga batas waktu habis, komponen tersebut dianggap gagal. Bentuk pemeriksaan yang paling sederhana adalah membuka koneksi TCP ke host dan port tujuan. Bila koneksi diterima, port dianggap terbuka, dan bila ditolak, layanan dianggap mati. Cara ini cepat dan ringan, tetapi hanya memastikan port dapat dijangkau, bukan bahwa aplikasi benar-benar mampu memproses permintaan. Batas waktu pun harus dipilih dengan cermat: terlalu singkat membuat node yang sehat dianggap mati, sedangkan terlalu lama membuat kegagalan terdeteksi terlambat.</p>

<p align="justify">Sebagian kegagalan koneksi hanya bersifat sementara, misalnya ketika server sedang restart atau jaringan sedang padat. Retry mengulang permintaan yang gagal sehingga gangguan singkat tidak langsung berubah menjadi error bagi pengguna. Namun pengulangan tanpa jeda dapat memperparah keadaan, karena server yang sedang pulih langsung dibanjiri permintaan. Exponential backoff mengatasinya dengan memperpanjang jeda pada setiap percobaan, dan jumlah percobaan dibatasi agar proses tidak menggantung. Tidak semua kegagalan layak diulang. Error koneksi umumnya bersifat sementara, sedangkan respons 4xx atau 5xx sering menandakan masalah yang tidak akan hilang meski permintaan dikirim lagi.</p>

<p align="justify">Retry hanya efektif selama gangguan berlangsung singkat. Jika layanan benar-benar mati, mengulang permintaan hanya membuang waktu dan menahan sumber daya. Circuit breaker mencatat riwayat kegagalan dan memutus alur permintaan setelah ambang tertentu terlampaui. Pada kondisi closed, permintaan diteruskan dan setiap kegagalan dihitung. Begitu ambang tercapai, kondisi berpindah ke open dan permintaan berikutnya langsung ditolak tanpa menghubungi layanan. Setelah waktu tunggu berakhir, kondisi berubah menjadi half-open untuk menguji apakah layanan sudah pulih. Bila uji berhasil, kondisi kembali ke closed, dan bila gagal, kembali ke open. Pada praktikum ini ambangnya empat kegagalan dengan waktu tunggu 20 detik, dan keempat mekanisme dipakai bersamaan agar terlihat jenis kegagalan apa yang ditangani oleh masing-masing.</p>

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
<p align="justify">Perintah uv python list dijalankan untuk melihat daftar versi Python yang tersedia dan yang sudah terpasang di komputer. Versi dengan lokasi python.exe berwarna biru sudah terpasang, yaitu CPython 3.15.0, 3.14.8, 3.14.4, dan 3.13.0 (di Laragon). Versi bertanda <download available> belum terpasang tetapi bisa diunduh uv, misalnya CPython 3.12 sampai 3.8, PyPy, dan GraalPy. Daftar ini membantu memilih versi yang tepat untuk proyek sebelum membuat virtual environment. Pada tugas ini dipilih CPython 3.14.4.</download>

### Insatl Pin python

<img width="431" height="92" alt="04" src="https://github.com/user-attachments/assets/2bd54f32-0741-4314-8571-e85e30ea104f" />

#### Pembahasan 

<p align="justify">Perintah uv python install 3.14.4 mengunduh dan memasang CPython 3.14.4 untuk Windows x86_64, dan prosesnya selesai dalam 20,47 detik. Perintah uv python pin 3.14.4 kemudian menulis versi tersebut ke file .python-version di folder proyek. Dengan begitu, uv akan selalu memakai Python 3.14.4 untuk proyek ini, sehingga lingkungan pengembangan konsisten dan tidak berubah saat dijalankan di komputer lain.</p>

### Buat virtual environment

<img width="413" height="71" alt="05_virtual-environment" src="https://github.com/user-attachments/assets/e6c75d0b-1676-4fa7-a693-a0c78fb5f2f4" />


#### Pembahasan

<p align="justify">Perintah uv venv membuat virtual environment di folder .venv dengan memakai CPython 3.14.4, sesuai versi yang sebelumnya dikunci. Virtual environment memisahkan paket-paket proyek dari instalasi Python global, sehingga dependensi tidak saling bentrok antarproyek. Pesan “Activate with: .venv\Scripts\activate” menunjukkan perintah yang harus dijalankan berikutnya untuk mengaktifkan lingkungan tersebut sebelum memasang paket.</p>

### Aktivasi virtual environment

<img width="353" height="58" alt="06_Aktivasi virtual environment" src="https://github.com/user-attachments/assets/21862877-26bb-4e10-af2d-d9239557cfc2" />

#### Pembahasan

<p align="justify">Perintah .venv\Scripts\activate mengaktifkan virtual environment yang sebelumnya dibuat. Setelah aktif, prompt berubah dengan awalan (workspace-05) yang menandakan terminal sekarang bekerja di dalam lingkungan virtual tersebut. Semua paket Python yang dipasang setelah ini hanya akan masuk ke environment proyek ini, sehingga tidak memengaruhi instalasi Python global di komputer.</p>



### Instal blacksheep

<img width="471" height="299" alt="07_install-blacksheep" src="https://github.com/user-attachments/assets/c9a0deb1-5b7a-45a8-9fda-7aaea6f84336" />

#### Pembahasan

<p align="justify">Perintah uv pip install blacksheep memasang framework BlackSheep versi 2.6.4 di dalam virtual environment yang aktif. uv me-resolve 14 paket dalam 1,76 detik, menyiapkan 12 paket dalam 2,28 detik, lalu memasangnya hanya dalam 257 ms. Selain BlackSheep, ikut terpasang dependensi pendukungnya, seperti httptools, h11, h2, hpack, dan hyperframe untuk pemrosesan HTTP, rodi untuk dependency injection, guardpost untuk autentikasi dan otorisasi, serta essentials-openapi untuk dokumentasi API. Dengan terpasangnya paket ini, framework siap dipakai untuk membangun aplikasi web.</p>

### Install Blacksheep cli

<img width="333" height="340" alt="08_install-blacksheep-cli" src="https://github.com/user-attachments/assets/98552784-444b-404d-9c89-6de482d32c30" />

#### Pembahasan

<p align="justify">Pada tahap ini virtual environment diaktifkan melalui PowerShell dengan .venv\Scripts\Activate.ps1, lalu dijalankan uv pip install blacksheep blacksheep-cli. Perintah ini memasang framework BlackSheep 2.6.4 dan BlackSheep CLI 0.0.5 beserta 41 paket yang di-resolve dalam 2,29 detik dan dipasang dalam 1,74 detik. CLI diperlukan untuk membuat kerangka proyek lewat perintah blacksheep create. Paket pendukungnya meliputi click, rich, questionary, dan prompt-toolkit untuk antarmuka terminal interaktif, cookiecutter dan jinja2 untuk pembuatan proyek dari template, serta essentials-configuration dan essentials-openapi untuk konfigurasi dan dokumentasi API. Paket HTTP seperti h11, h2, dan httptools juga ikut terpasang.</p>

### Buat Proyek Blacksheep

<img width="398" height="101" alt="09_buat-proyek-blacksheep" src="https://github.com/user-attachments/assets/d2958093-b864-4a4d-afe8-99bc7591d8e7" />

#### Pembahasan

<p align="justify">Perintah blacksheep create membuat kerangka proyek baru secara interaktif. Pilihan yang dipakai adalah nama proyek blacksheep_lb, template mvc (struktur Model-View-Controller), dokumentasi OpenAPI diaktifkan, pustaka pembaca pengaturan essentials-configuration, dan format pengaturan aplikasi TOML. Setelah selesai, muncul pesan “Project created in blacksheep_lb” disertai langkah berikutnya: masuk ke folder proyek dengan cd blacksheep_lb, memasang dependensi dengan pip install -r requirements.txt, lalu menjalankan aplikasi dengan python dev.py.</p>

### Instal requirements

<img width="352" height="170" alt="10_install-requirements" src="https://github.com/user-attachments/assets/314e35e4-4b33-4338-a22d-16a035b6e0f6" />

#### Pembahasan

<p align="justify">Setelah proyek dibuat, dilakukan perpindahan ke folder blacksheep_lb dengan cd, lalu dijalankan uv pip install -r requirements.txt untuk memasang dependensi proyek di lingkungan Python 3.14.8 pada .venv. uv me-resolve 37 paket dalam 1,59 detik, membangun ulang markupsafe 3.0.2, lalu memasang 13 paket dalam 274 ms. Paket yang terpasang antara lain uvicorn sebagai server ASGI, pydantic untuk validasi data, cryptography dan pyjwt untuk keamanan dan token, serta websockets untuk komunikasi dua arah. Versi markupsafe diturunkan dari 3.0.4 ke 3.0.2 menyesuaikan kebutuhan berkas requirements.txt.</p>

### Jalankan aplikasi

<img width="350" height="64" alt="11_Jalamkan_aplikasi" src="https://github.com/user-attachments/assets/215b828a-9728-4441-8c6d-4d0fcaaa4c00" />

#### Pembahasan 

<p align="justify">Perintah python dev.py dijalankan dari folder blacksheep_lb untuk memulai aplikasi dalam mode pengembangan lokal. Terminal menampilkan “Running for local development” beserta alamat http://localhost:44777/ yang bisa dibuka di browser. Log menunjukkan server berhasil dimulai (server process 34060), menunggu startup aplikasi, lalu “Application startup complete”. Artinya aplikasi berjalan tanpa galat dan siap diakses.</p>

### Jalankan aplikasi autoreload

<img width="637" height="119" alt="12_jalankan-aplikasi-autoreload" src="https://github.com/user-attachments/assets/8282ea57-8eef-441c-a499-cbe55d5b6ea4" />

#### Pembahasan

<p align="justify">Perintah python dev.py kembali dijalankan dari folder blacksheep_lb, dan kali ini aplikasi berjalan dengan fitur auto-reload. Log menunjukkan Uvicorn memantau perubahan file di direktori proyek, lalu memulai reloader process (5008) dengan StatReload dan server process (10416). Setiap perubahan kode akan membuat server dimuat ulang otomatis tanpa perlu dijalankan ulang secara manual. Alamat yang ditampilkan adalah http://localhost:44777/docs/, yaitu dokumentasi API interaktif berbasis OpenAPI. Pesan “Application startup complete” menandakan aplikasi siap diakses.</p>

### Tampilan halaman utama

<img width="808" height="364" alt="13_tampilan-halaman-utama" src="https://github.com/user-attachments/assets/d8417043-c0d6-434b-a19d-4cef3fef0112" />


#### Pembahasan

<p align="justify">Alamat localhost:44777 dibuka di browser dan menampilkan halaman utama aplikasi BlackSheep. Halaman ini memuat menu navigasi Getting Started, About, Contact, dan OpenAPI Docs, serta deskripsi bahwa BlackSheep adalah framework web asinkron untuk membangun aplikasi Python yang berbasis event dan non-blocking. Di bawahnya tertulis bahwa BlackSheep adalah framework ASGI yang cepat sekaligus HTTP client untuk Python asyncio. Tampilan ini membuktikan bahwa proyek hasil template MVC berhasil dijalankan dan dapat diakses melalui browser.</p>

### Log permintaan http

<img width="446" height="275" alt="14_log-permintaan-http" src="https://github.com/user-attachments/assets/bf04a491-4952-4ea3-871a-6e16db7526d7" />


#### Pembahasan

<p align="justify">Setelah server berjalan dan halaman dibuka di browser, terminal menampilkan log permintaan HTTP yang masuk ke Uvicorn di http://localhost:44777. Permintaan GET / dari browser diikuti permintaan file pendukung halaman, seperti CSS (all.min.css, public.css), gambar (blacksheep.png, favicon), JavaScript (jquery.min.js, bootstrap.bundle.min.js, freelancer.js), dan font Font Awesome (.woff2). Semua permintaan berstatus 200 OK, sehingga seluruh file statis berhasil dimuat tanpa galat. Pengulangan permintaan GET / menunjukkan halaman dimuat ulang beberapa kali. Log ini membuktikan bahwa aplikasi merespons permintaan dengan benar.</p>


### Struktur proyek

<img width="347" height="230" alt="15_struktur-proyek" src="https://github.com/user-attachments/assets/88c9f317-9fce-4533-80d0-b1a91d0100e6" />

#### Pembahasan

<p align="justify">Perintah cd blacksheep_lb dijalankan untuk masuk ke folder proyek, lalu Get-ChildItem -Force menampilkan seluruh isinya, termasuk file tersembunyi. Proyek terdiri dari tiga folder, yaitu app (controller, view, dan konfigurasi aplikasi), domain (logika bisnis), dan tests (pengujian). File pentingnya adalah dev.py sebagai titik masuk server pengembangan, Dockerfile untuk membangun image container, requirements.txt untuk daftar dependensi, serta settings.toml dan settings.dev.toml untuk konfigurasi aplikasi. Ada juga .dockerignore, .gitignore, .flake8, pyproject.toml, dan README.md yang mendukung pengelolaan Docker, repositori, gaya kode, dan dokumentasi proyek.</p>

### Build docker compose

<img width="377" height="354" alt="16_build-docker-compose" src="https://github.com/user-attachments/assets/f1011784-bbb2-4605-b59c-e9d9aae594f3" />

<img width="350" height="251" alt="17_Build_docker_compose" src="https://github.com/user-attachments/assets/72d284b2-e1a3-474e-a48f-b74f6361a336" />


#### Pembahasan

<p align="justify">Di dua gambar ini terlihat proses menjalankan seluruh sistem dengan satu perintah Docker Compose. Awalnya Docker mengunduh bahan-bahan yang dibutuhkan, yaitu image Nginx dan Python, lalu memasang beberapa paket tambahan. Bagian ini paling lama, sekitar dua menit. Setelah itu Nginx disiapkan dengan file konfigurasi sendiri, dan aplikasi BlackSheep dibangun lengkap dengan lingkungan Python serta dependensinya. Di bagian akhir, semuanya selesai tanpa galat: dua image berhasil dibuat, jaringan khusus untuk komunikasi antarcontainer terbentuk, dan tiga container langsung berjalan, yaitu dua instance aplikasi (bs_app-1 dan bs_app-2) serta satu Nginx. Jadi ketika pengguna membuka aplikasi, permintaannya diterima Nginx lebih dulu, lalu dibagi ke salah satu dari dua aplikasi tersebut. Dengan cara ini kerja server terbagi rata, dan kalau salah satu aplikasi bermasalah, yang lain masih bisa melayani pengguna.</p>


---

# KESIMPULAN

<p align="justify">Praktikum ini membuktikan bahwa load balancing dengan nginx di depan dua replika aplikasi (bs_app-1 dan bs_app-2) berjalan baik: pengguna cukup mengakses satu alamat di port 80, lalu request dibagi secara round-robin dan terbukti lewat log kedua replika. Untuk deteksi kegagalan, check-server.py hanya menunjukkan port terbuka atau tertutup sehingga cocok sebagai indikator awal. Retry menangani gangguan koneksi singkat dengan jeda yang makin panjang, sedangkan circuit breaker berhenti menghubungi layanan setelah ambang kegagalan tercapai, sehingga saat server mati retry mencoba lima kali dan circuit breaker hanya sekali. Konfigurasi yang dipakai masih sederhana karena nginx belum memeriksa kesehatan tiap instance dan perpindahan kondisi open dan half-open belum teramati, jadi untuk penggunaan nyata perlu ditambahkan health check pada upstream dan pemanggilan yang berulang.</p>


---
# REFERENSI

1. Bambang Purnomosidi D. P. (2026). Modul 5: Fault Tolerance. Praktikum Sistem Terdistribusi dan Terdesentralisasi, Prodi Informatika, Universitas Teknologi Digital Indonesia.
2. Neoteroi. BlackSheep documentation. https://www.neoteroi.dev/blacksheep/
3. nginx. Module ngx_http_upstream_module. https://nginx.org/en/docs/http/ngx_http_upstream_module.html
4. nginx. HTTP load balancing. https://docs.nginx.com/nginx/admin-guide/load-balancer/http-load-balancer/
5. Docker. Compose file reference. https://docs.docker.com/compose/compose-file/
6. Docker. docker compose up. https://docs.docker.com/reference/cli/docker/compose/up/
7. jd. tenacity. https://github.com/jd/tenacity
8. Daniel F. Martins. pybreaker. https://github.com/danielfm/pybreaker
9. Stack Overflow. How to check whether my server is up and running using python. https://stackoverflow.com/questions/20867184/
10. Microsoft. Circuit Breaker pattern. https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
11. Astral. uv documentation. https://docs.astral.sh/uv/


