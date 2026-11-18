# Praktikum Minggu MODUL 07 - Cloud Computing


| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi | 
| **Topik** | Cloud Computing |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 | 
| **Kelas** | IF-1 |

---

#  TUJUAN PRAKTIKUM

---
#  DASAR TEORI

---
#  PEMBAHASAN
### source

### 1. Membuat env Python 3.14.4

Salin satu persatu kode dibawah ini:

```python
uv python install 3.14.4
uv venv --python 3.14.4
.venv\Scripts\activate.bat
python --version
```

<img width="522" height="163" alt="03" src="https://github.com/user-attachments/assets/080bd638-2eec-46d4-909e-cff2973c3fb3" />

#### Pembahasan

<p align="justify">Perintah-perintah di terminal ini berhasil menyiapkan lingkungan Python 3.14.4 untuk proyek flask-app Anda menggunakan uv: uv python install 3.14.4 memastikan Python versi tersebut sudah terpasang (hasilnya “already installed”, jadi tidak perlu mengunduh ulang), lalu uv venv --python 3.14.4 membuat virtual environment di folder .venv, dan karena folder tersebut sudah ada, uv menanyakan apakah ingin menggantinya dan Anda menjawab “yes” sehingga .venv lama dibuat ulang dari awal. Setelah itu, .venv\Scripts\activate.bat mengaktifkan environment tersebut (ditandai prefiks (flask-app) di prompt), dan python --version mengonfirmasi bahwa Python yang aktif adalah 3.14.4, artinya environment sudah siap dipakai untuk menginstal dependensi seperti Flask dengan uv pip install flask.</p>


### 2. Install Paket yang Diperlukan

```python
uv pip install -e .
```

<img width="419" height="158" alt="04_uv_pip_install" src="https://github.com/user-attachments/assets/c366c1ca-2ee7-4965-8936-f1d14c053c01" />

#### Pembahasan

<p align="justify">Perintah uv pip install -e . berhasil memasang proyek flaskr Anda dalam mode editable (-e), artinya paket dipasang sebagai tautan ke folder proyek sehingga setiap perubahan pada kode langsung berlaku tanpa perlu instal ulang. uv me-resolve 8 paket dalam 2,27 detik, membangun flaskr versi 1.0.0 dari folder lokal, lalu memasang semuanya dalam 157 ms: selain flaskr sendiri, terpasang flask 3.1.3 beserta dependensinya, yaitu werkzeug (penangan WSGI dan routing), jinja2 (mesin template), click (antarmuka perintah CLI), itsdangerous (penandatanganan data seperti session), markupsafe (pengamanan teks pada template), dan blinker (sistem sinyal/event). Dengan begitu, aplikasi Flask Anda sudah siap dijalankan, misalnya dengan flask --app flaskr run --debug.</p>

```python
flask --app flaskr init-db
flask --app flaskr run
```

<img width="725" height="97" alt="05_flask" src="https://github.com/user-attachments/assets/201dd2a5-3a7a-4116-9ec5-bd795ef16741" />

#### Pembahasan

<p align="justify">Perintah flask --app flaskr init-db berhasil membuat dan menginisialisasi database aplikasi (ditandai pesan “Initialized the database”), biasanya dengan menjalankan skema SQL yang menghasilkan file SQLite di folder instance. Setelah itu, flask --app flaskr run menjalankan aplikasi flaskr pada server pengembangan bawaan Flask yang dapat diakses di http://127.0.0.1:5000 (localhost, port 5000), sehingga Anda bisa membukanya lewat browser. Pesan Debug mode: off berarti mode debug tidak aktif, jadi server tidak akan memuat ulang otomatis saat kode diubah dan tidak menampilkan debugger interaktif jika terjadi error; untuk pengembangan, tambahkan --debug. Peringatan berwarna merah hanyalah pengingat bahwa server ini khusus untuk pengembangan, bukan untuk produksi, yang seharusnya memakai server WSGI seperti Gunicorn atau Waitress.</p>


<img width="463" height="215" alt="06_Register" src="https://github.com/user-attachments/assets/2ceee64f-b120-4c8d-8ea8-0870ae772540" />

#### Pembahasan

<p align="justify">Gambar ini menunjukkan halaman Register aplikasi Flaskr yang sudah berjalan di browser, berisi formulir pendaftaran dengan kolom Username (terisi “Mexi”) dan Password (terisi enam karakter yang disamarkan menjadi titik-titik), serta tombol Register untuk mengirimkan data. Saat tombol diklik, aplikasi akan memeriksa bahwa kedua kolom terisi dan username belum dipakai, lalu menyimpan akun ke database SQLite dengan password yang sudah di-hash (bukan disimpan sebagai teks asli), dan mengarahkan Anda ke halaman Log In. Bagian header menampilkan tautan Register dan Log In karena pengguna belum login; setelah login, tautan itu akan berganti menjadi nama pengguna dan Log Out, sehingga Anda bisa lanjut membuat dan mengelola post di blog Anda.</p>


<img width="468" height="233" alt="07_Login" src="https://github.com/user-attachments/assets/149d4521-c970-47f7-9156-9f0f3dce5861" />

#### Pembahasan

<p align="justify">Ini tampilan halaman Log In di Flaskr, yang muncul otomatis setelah proses registrasi berhasil. Di sini saya mengisi username “Mexi” dan password yang sama dengan waktu mendaftar, lalu menekan tombol Log In. Aplikasi akan mengecek apakah username-nya ada di database dan apakah password yang diketik cocok dengan hash yang tersimpan. Kalau cocok, ID pengguna disimpan di session sehingga aplikasi tahu saya sudah login, lalu saya diarahkan ke halaman utama. Kalau salah, muncul pesan error di halaman yang sama. Setelah berhasil masuk, tampilan header berubah: tautan Register dan Log In diganti nama pengguna dan Log Out, dan muncul tautan New untuk membuat post baru.</p>

<img width="464" height="103" alt="08_Hasil" src="https://github.com/user-attachments/assets/21927787-bee2-465c-90ee-771778777ad2" />

#### Pembahasan

<p align="justify">Setelah login berhasil, saya langsung diarahkan ke halaman utama Flaskr yang judulnya “Posts”. Di bagian header, tautan Register dan Log In sudah berganti menjadi nama saya, “Mexi”, dan tautan Log Out, jadi ini menandakan aplikasi sudah mengenali saya lewat session. Daftar post masih kosong karena belum ada tulisan yang dibuat, dan di sebelah kanan judul ada tautan New yang bisa diklik untuk membuat post pertama. Dari sini, proses autentikasi bisa dibilang sudah berjalan dengan baik, mulai dari registrasi, login, sampai tampilan halaman utama untuk pengguna yang sudah masuk.</p>


<img width="714" height="300" alt="09_Hasil_tes_lokal" src="https://github.com/user-attachments/assets/c11b8933-41cb-4bc0-9e3d-a274b1626c91" />

#### Pembahasan

<p align="justify">Ini log terminal yang mencatat semua aktivitas saya di aplikasi Flaskr tadi, dan urutannya cocok dengan langkah yang sudah saya lakukan. Pertama, GET / dengan status 200 menandakan halaman utama berhasil dimuat, disusul style.css yang juga berhasil diambil, sedangkan favicon.ico bernilai 404 karena aplikasi memang belum punya ikon situs, jadi itu bukan error yang perlu dikhawatirkan. Lalu GET /auth/register (200) menampilkan formulir pendaftaran, dan POST /auth/register dengan status 302 berarti data berhasil dikirim dan saya dialihkan ke halaman login (GET /auth/login, 200). Setelah itu POST /auth/login juga berstatus 302, artinya login berhasil dan saya diarahkan kembali ke GET / (200). Terakhir, GET /auth/logout (302) menunjukkan saya keluar dari akun dan kembali ke halaman utama. Kode 304 pada style.css berarti browser memakai versi cache karena file tidak berubah, sehingga seluruh alur registrasi, login, dan logout sudah berjalan normal.</p>

### 3. Buat Aplikasi Menjadi CA - Docker

Buat Dockerfile

```python
(
echo FROM python:3.14
echo.
echo RUN mkdir /app
echo WORKDIR /app
echo ADD . /app/
echo RUN pip install -e .
echo RUN flask --app flaskr init-db
echo.
echo EXPOSE 5000
echo CMD ["flask", "--app", "flaskr", "run", "--host=0.0.0.0", "--port=5000"]
) > Dockerfile
```

<img width="516" height="149" alt="10_Buat_Dockerfile" src="https://github.com/user-attachments/assets/ea31eeaa-b072-4848-92e0-f807c1b7c748" />

#### Pembahasan

<p align="justify">Di sini saya membuat file Dockerfile langsung dari Command Prompt dengan memakai blok ( ... ) > Dockerfile, di mana setiap perintah echo menulis satu baris isi file tersebut, dan echo. menghasilkan baris kosong sebagai pemisah. Isinya menyusun image untuk aplikasi Flaskr: dimulai dari image dasar python:3.14, membuat dan menetapkan /app sebagai direktori kerja, menyalin seluruh isi proyek ke dalamnya dengan ADD . /app/, lalu menjalankan pip install -e . untuk memasang aplikasi beserta dependensinya dan flask --app flaskr init-db untuk menyiapkan database di dalam image. Baris EXPOSE 5000 menandai port yang dipakai aplikasi, dan CMD menjalankan Flask dengan --host=0.0.0.0 agar server bisa diakses dari luar container (bukan hanya dari localhost di dalam container), sehingga nanti image ini bisa dibangun dengan docker build -t flaskr . dan dijalankan dengan docker run -p 5000:5000 flaskr.</p>

Buat .dockerignore, supaya .venv Windows tidak ikut masuk ke image Linux:

```python
(
echo .venv
echo __pycache__
echo instance
echo *.pyc
) > .dockerignore
```

<img width="372" height="84" alt="11_Buat_dockerignore" src="https://github.com/user-attachments/assets/6f6760f7-8eaf-4f4c-91fa-14be85090911" />

#### Pembahasan

<p align="justify">Di langkah ini saya membuat file .dockerignore dengan cara yang sama seperti Dockerfile tadi, yaitu blok ( ... ) > .dockerignore yang menulis satu entri per baris. Isinya empat hal yang sengaja tidak ikut disalin ke image saat perintah ADD . /app/ berjalan: folder .venv (virtual environment lokal yang tidak cocok dibawa ke container karena path dan platformnya berbeda, ditambah ukurannya besar), __pycache__ dan *.pyc (file cache bytecode Python yang dibuat otomatis dan tidak perlu disalin), serta folder instance yang berisi database SQLite lokal saya. Dengan begitu, image menjadi lebih kecil, proses build lebih cepat, dan database di dalam container dibuat bersih lewat flask --app flaskr init-db pada Dockerfile, bukan membawa data akun dari komputer saya.</p>

Cek isinya

```python
type Dockerfile
```

<img width="447" height="139" alt="12_Cek_Isi" src="https://github.com/user-attachments/assets/7c3f2221-8669-4084-a701-6a8dac8cd246" />

#### Pembahasan

<p align="justify">Di sini saya menjalankan type Dockerfile untuk mengecek isi file yang tadi dibuat lewat blok echo, dan hasilnya sudah sesuai: semua baris tertulis rapi, dengan baris kosong tepat di tempat echo. dipakai sebagai pemisah. Isinya berurutan dari image dasar python:3.14, pembuatan direktori /app dan penetapannya sebagai WORKDIR, penyalinan proyek dengan ADD . /app/, pemasangan aplikasi lewat pip install -e ., dan inisialisasi database dengan flask --app flaskr init-db. Bagian akhirnya EXPOSE 5000 dan CMD yang menjalankan Flask di 0.0.0.0 port 5000 supaya bisa diakses dari luar container. Karena file ini sudah benar, langkah berikutnya adalah membangun image dengan docker build -t flaskr . lalu menjalankannya dengan docker run -p 5000:5000 flaskr.</p>

Build dan cek image

```python
docker build -f Dockerfile -t flaskr:1.0.0 .
docker image ls
```

<img width="469" height="290" alt="13_Build" src="https://github.com/user-attachments/assets/6f5e70cb-ce54-40c6-a05b-090caddab88f" />

#### Pembahasan

<p align="justify">Saya menjalankan docker build -f Dockerfile -t flaskr:1.0.0 . dan prosesnya selesai dalam 20,3 detik (11 dari 11 langkah, status FINISHED), jadi image berhasil dibuat tanpa error. Docker mulai dengan membaca Dockerfile dan .dockerignore, mengambil metadata image dasar python:3.14, lalu mengirim konteks build yang hanya berukuran sekitar 42,93 kB, kecil karena .venv, instance, dan file cache sudah dikecualikan. Setelah itu keenam instruksi Dockerfile dijalankan berurutan: membuat /app, menetapkan WORKDIR, menyalin proyek, memasang aplikasi lewat pip install -e . (langkah terlama, sekitar 11,7 detik karena mengunduh dependensi), dan menginisialisasi database. Di tahap akhir, Docker mengekspor layer dan menyimpan hasilnya dengan nama docker.io/library/flaskr:1.0.0, sehingga image sudah siap dijalankan dengan docker run -p 5000:5000 flaskr:1.0.0 lalu diakses lewat http://localhost:5000.</p>


<img width="472" height="131" alt="14_Cek_Image" src="https://github.com/user-attachments/assets/506c0d48-ad76-41c3-b743-36ed79340b59" />

#### Pembahasan

<p align="justify">Saya menjalankan docker image ls untuk memastikan image hasil build tadi benar-benar tersimpan, dan flaskr:1.0.0 muncul di daftar dengan ID 5a26919f69b8, memakai ruang disk 1,64 GB dengan ukuran konten sekitar 423 MB. Ukurannya cukup besar karena image dasar python:3.14 versi penuh sudah membawa banyak paket sistem, dan kalau ingin lebih ringan, bisa diganti dengan varian python:3.14-slim. Selain itu ada dua image lain dari proyek sebelumnya, yaitu workspace-05-bs_app:latest (502 MB) dan workspace-05-nginx:latest (241 MB), yang tidak ada hubungannya dengan Flaskr. Kolom “In Use” belum menunjukkan tanda apa pun, artinya belum ada container yang berjalan dari image flaskr, jadi langkah selanjutnya adalah menjalankannya dengan docker run -p 5000:5000 flaskr:1.0.0 lalu mengaksesnya di http://localhost:5000.</p>

### 4. Menjalankan Image

```python
docker run -p 5001:5000 flaskr:1.0.0
```

<img width="716" height="141" alt="15_jalankan" src="https://github.com/user-attachments/assets/ee3a4215-e495-4121-b6e3-f6be0b2f85f3" />

#### Pembahasan

<p align="justify">Saya menjalankan docker run -p 5001:5000 flaskr:1.0.0 dan container berhasil hidup: Flask melayani aplikasi flaskr di dalam container pada port 5000, sedangkan opsi -p 5001:5000 memetakannya ke port 5001 di komputer saya, jadi aplikasinya dibuka lewat http://localhost:5001, bukan 5000 (tidak bentrok dengan server Flask lokal tadi). Baris “Running on all addresses (0.0.0.0)” muncul karena CMD memakai --host=0.0.0.0, dan alamat 172.17.0.2:5000 adalah IP internal container di jaringan Docker. Log di bawahnya menunjukkan permintaan pertama dari 172.17.0.1 (gateway Docker, yaitu browser saya yang masuk lewat port mapping): GET / dan style.css berstatus 200 yang berarti halaman berhasil tampil, sedangkan favicon.ico 404 hanya karena aplikasi belum punya ikon situs. Peringatan merah tetap sama, yaitu server ini khusus pengembangan dan untuk produksi sebaiknya memakai Gunicorn atau Waitress. Karena database dibuat ulang saat build, akun yang saya daftarkan sebelumnya tidak ikut terbawa, jadi di container ini saya perlu mendaftar lagi.</p>


<img width="464" height="102" alt="16_Tampilan_hasil" src="https://github.com/user-attachments/assets/22bb2240-b86d-4188-a7d1-205aa498bf65" />

#### Pembahasan

<p align="justify">Ini tampilan halaman utama Flaskr yang saya buka dari container Docker lewat http://localhost:5001, dan aplikasinya berhasil tampil dengan benar. Di header masih muncul tautan Register dan Log In, bukan nama “Mexi”, karena ini adalah database baru yang dibuat ulang saat build image, sehingga akun yang saya daftarkan sebelumnya di server lokal tidak ikut terbawa. Daftar post juga masih kosong dan tidak ada tautan New karena saya belum login. Hal ini membuktikan bahwa container berjalan terpisah dari server lokal, dengan database sendiri di dalamnya, dan proses containerisasi aplikasi Flaskr dengan Docker sudah berhasil dari build, run, sampai diakses lewat browser.</p>

### 5. Buat Aplikasi Menjadi CA - Podman
Podman

```python
winget install --id RedHat.Podman -e
```

<img width="461" height="122" alt="17_Podman" src="https://github.com/user-attachments/assets/f294ff80-3424-48b7-a7c3-1d7b51bab855" />

#### Pembahasan

<p align="justify">Saya menjalankan winget install RedHat.Podman untuk memasang Podman, yaitu alternatif Docker dari Red Hat yang perintahnya hampir sama, tetapi winget melaporkan bahwa paket tersebut sudah terpasang sebelumnya. Karena itu winget otomatis mencoba memperbaruinya, lalu menampilkan “No available upgrade found” dan “No newer package versions are available”, artinya Podman yang ada sudah versi terbaru dan tidak ada yang perlu diunduh atau diubah. Perhatikan juga bahwa prompt di sini sudah tidak memakai prefiks (flask-app), jadi virtual environment tidak aktif, tetapi hal itu tidak berpengaruh karena Podman adalah aplikasi sistem. Langkah selanjutnya adalah menyiapkan mesin virtualnya dengan podman machine init dan podman machine start, lalu mengecek instalasi dengan podman --version sebelum membangun image Flaskr memakai Dockerfile yang sama lewat podman build -t flaskr:1.0.0 .</p>

```python
podman build -f Dockerfile -t flaskr:1.0.0 .
```

<img width="779" height="453" alt="18" src="https://github.com/user-attachments/assets/530943e2-8884-4daa-950d-173ba734cabd" />

<img width="956" height="339" alt="19" src="https://github.com/user-attachments/assets/982a8bee-17d1-4a18-a8ab-f808ca92c7e2" />

#### Pembahasan

<p align="justify">Saya menjalankan podman build -f Dockerfile -t flaskr:1.0.0 . dari terminal dengan prefiks (venv), dan Podman membangun image dalam 8 langkah (lebih banyak dari Docker yang menampilkan 6 karena Podman juga menghitung FROM, EXPOSE, dan CMD). Langkah 2 dan 3 (mkdir dan WORKDIR) memakai cache karena sudah pernah dijalankan, lalu ADD . /app/ menyalin proyek dan pip install -e . membangun aplikasi sambil mengunduh Flask beserta dependensinya (blinker, click, itsdangerous, jinja2, markupsafe, werkzeug). Pemasangan berhasil, dengan peringatan bahwa pip dijalankan sebagai root (wajar di dalam container) dan pemberitahuan versi pip baru yang bisa diabaikan. Setelah itu flask --app flaskr init-db menampilkan “Initialized the database”, EXPOSE 5000 dan CMD ditetapkan, dan image di-commit lalu diberi tag localhost/flaskr:1.0.0 dengan ID e2c6d8afb7c7, sehingga build dengan Podman berhasil dan hasilnya sama dengan build Docker sebelumnya.</p>


```python
podman image ls
```

<img width="494" height="81" alt="20" src="https://github.com/user-attachments/assets/32cffcdd-b597-4469-8cee-9b2a122f170c" />

#### Pembahasan

<p align="justify">Saya menjalankan podman image ls untuk memastikan hasil build tadi tersimpan, dan image localhost/flaskr dengan tag 1.0.0 muncul paling atas dengan ID e2c6d8afb7c7, dibuat 33 detik yang lalu, dan berukuran 1,18 GB, cocok dengan ID yang tercetak di akhir proses build sebelumnya. Di bawahnya ada dua image tanpa nama dan tag (<none>) yang merupakan sisa build lama (14 menit dan 5 hari lalu, masing-masing 1,16 GB), yaitu image yang namanya diambil alih oleh build terbaru sehingga tersisa tanpa label dan bisa dibersihkan dengan podman image prune bila ingin menghemat ruang. Baris terakhir adalah image dasar docker.io/library/python tag 3.14 (1,14 GB) yang diunduh dari Docker Hub dan dipakai pada instruksi FROM, sehingga ukuran image Flaskr hanya bertambah sekitar 40 MB dari image dasarnya. Image ini siap dijalankan dengan podman run -p 5001:5000 localhost/flaskr:1.0.0.</p>

```python
podman run -p 5001:5000 flaskr:1.0.0
```

<img width="713" height="116" alt="21" src="https://github.com/user-attachments/assets/236063e8-5ae9-4a98-b840-21f0fcad7b26" />

#### Pembahasan

<p align="justify">Saya menjalankan podman run -p 5001:5000 flaskr:1.0.0 dan container berhasil hidup: Flask melayani aplikasi flaskr pada port 5000 di dalam container, sedangkan opsi -p 5001:5000 memetakannya ke port 5001 di komputer saya, sehingga aplikasinya dibuka lewat http://localhost:5001. Baris “Running on all addresses (0.0.0.0)” muncul karena CMD memakai --host=0.0.0.0, dan alamat 192.168.116.184:5000 adalah IP internal container di jaringan Podman (berbeda dari Docker yang tadi menampilkan 172.17.0.2, karena Podman di Windows berjalan di dalam mesin virtual dengan jaringannya sendiri). Berbeda dengan log Docker, di sini belum ada baris permintaan GET karena browser belum membuka halaman, jadi log baru akan bertambah setelah alamat tersebut diakses. Peringatan merah tetap sama, yaitu server ini khusus pengembangan dan untuk produksi sebaiknya memakai Gunicorn atau Waitress, dan terminal akan terus “tertahan” selama container berjalan sampai dihentikan dengan CTRL+C.</p>


Buka http://127.0.0.1:5001. Jika Podman menanyakan registry untuk python:3.14, pilih docker.io.

<img width="472" height="106" alt="22" src="https://github.com/user-attachments/assets/a615ea9e-0ab7-414d-aae1-0e18a728697d" />

#### Pembahasan

<p align="justify">Ini tampilan halaman utama Flaskr yang saya buka dari container Podman lewat http://localhost:5001, dan aplikasinya berhasil tampil dengan benar. Header masih menampilkan tautan Register dan Log In, bukan nama pengguna, karena database di dalam container ini dibuat baru saat build image, sehingga tidak ada akun dari server lokal maupun container Docker sebelumnya. Daftar post juga masih kosong dan tautan New belum muncul karena saya belum login. Tampilannya identik dengan hasil di Docker, yang membuktikan bahwa Dockerfile yang sama bisa dibangun dan dijalankan di Docker maupun Podman dengan hasil yang konsisten.</p>


<img width="717" height="170" alt="23" src="https://github.com/user-attachments/assets/5161585b-3d6b-4163-94b5-cf7b6bcbce38" />

#### Pembahasan

<p align="justify">Ini log container Podman yang sama seperti sebelumnya, tetapi sekarang sudah terisi catatan permintaan setelah saya membuka http://localhost:5001 di browser. Permintaan pertama, GET / dengan status 200, menandakan halaman utama berhasil dimuat, disusul style.css (200) yang menampilkan tampilan halaman, sedangkan favicon.ico bernilai 404 karena aplikasi belum punya ikon situs, jadi itu bukan error yang perlu dikhawatirkan. Permintaan kedua pada pukul 18:44:32 (saya memuat ulang halaman) menunjukkan style.css berstatus 304, artinya browser memakai versi cache karena file tidak berubah. Semua permintaan tercatat berasal dari 192.168.116.184, yaitu alamat gateway jaringan Podman (mesin virtual tempat Podman berjalan di Windows), bukan alamat browser saya secara langsung, sama seperti 172.17.0.1 pada log Docker tadi. Ini membuktikan container Podman benar-benar melayani permintaan dari browser dan aplikasi Flaskr berjalan baik di Podman.</p>


---
# KESIMPULAN

---
# REFERENSI
