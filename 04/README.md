# Praktikum Minggu MODUL 04 - Konsistensi dan Replikasi pada Sistem Terdistribusi

| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi |
| **Topik** | Konsistensi dan Replikasi pada Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 | 
| **Kelas** | IF-1 |

---

#  TUJUAN PRAKTIKUM

- Memahami konsep konsistensi dan replikasi data dalam sistem terdistribusi.
- Membedakan replikasi sinkron dan asinkron, serta model primary-replica dan master-master.
- Membangun streaming replication PostgreSQL 18 dengan satu primary dan satu replica memakai Docker Compose.
- Mengkaji fungsi WAL, physical replication slot, dan pg_basebackup -R dalam proses sinkronisasi data.
- Memeriksa status replikasi lewat tabel diagnostik, lalu menguji perubahan data pada kedua node.
- Mensimulasikan High Availability dengan mempromosikan replica menjadi primary.
- Menyiapkan cluster master-master Apache Ignite 3 dan membuktikan bahwa tiap node dapat membaca sekaligus menulis data.
  
---

#  DASAR TEORI

### Replikasi dan Konsistensi

<p align="justify">Menyimpan data di satu mesin berarti satu kerusakan bisa mematikan seluruh layanan. Replikasi menyimpan salinan data di beberapa node agar layanan tetap hidup saat satu node gagal, beban baca terbagi, dan data bisa ditaruh dekat pengguna. Konsekuensinya, semua salinan harus selaras, dan di sinilah model konsistensi berperan. Konsistensi kuat menjamin pembacaan selalu melihat tulisan terakhir, tetapi operasi tulis harus menunggu koordinasi antar node. Konsistensi eventual membolehkan salinan tertinggal sebentar asalkan akhirnya seragam, sehingga lebih cepat namun bisa menampilkan data lama. Menurut teorema CAP, saat jaringan terpisah sistem harus memilih antara tetap konsisten atau tetap tersedia.</p>

### Primary-Replica dan Streaming Replication

<p align="justify">Pada model ini hanya primary yang menerima tulisan, sedangkan replica menyalin perubahan dan melayani pembacaan. Karena penulisnya tunggal, tidak ada konflik tulis, dan replica bisa menggantikan primary bila gagal. Pada replikasi sinkron, primary menunggu konfirmasi replica sebelum commit sehingga data tidak hilang, tetapi tulis lebih lambat. Pada replikasi asinkron, primary langsung commit dan mengirim perubahan belakangan, sehingga lebih cepat namun transaksi terakhir bisa belum sampai ke replica. Streaming replication berarti perubahan dialirkan terus-menerus, bukan dikirim sebagai snapshot berkala.</p>

### WAL, LSN, dan Replication Slot

<p align="justify">Di PostgreSQL, setiap perubahan dicatat lebih dulu ke Write-Ahead Log (WAL) sebelum data diperbarui. WAL semula untuk pemulihan setelah crash, lalu dipakai juga untuk replikasi: WAL sender di primary mengalirkan WAL, WAL receiver di replica menerimanya dan memutar ulang hingga datanya identik. Posisi di dalam WAL ditandai dengan LSN, dan selisih posisi kirim dengan posisi replay disebut lag replikasi. Replication slot menahan WAL di primary sampai replica mengonfirmasi penerimaan, tetapi jika replica mati lama, WAL dapat menumpuk dan memenuhi disk.</p>

### High Availability dan Failover

<p align="justify">Replikasi hanya menyediakan data cadangan, sedangkan pemulihan layanan dilakukan lewat failover, yaitu memindahkan peran primary ke replica. Failover bisa manual dengan pg_promote() atau otomatis dengan alat seperti Patroni dan repmgr. Risiko terbesarnya adalah split-brain, yaitu dua node sama-sama merasa sebagai primary sehingga datanya bercabang. Sistem produksi mencegahnya dengan fencing, sedangkan pada praktikum ini primary lama cukup dihentikan dan tidak dinyalakan lagi sebagai primary.</p>

### Apache Ignite 3 dan Master-Master

<p align="justify">Ignite 3 menyimpan data di memori dan disk, dibagi menjadi partisi yang ditempatkan di node sesuai zona. Zona juga menentukan replication factor, yaitu jumlah salinan data. Semua node setara karena masing-masing bisa membaca dan menulis, dan permintaan untuk partisi milik node lain diteruskan otomatis. Metadata cluster dikelola dengan consensus sehingga perubahan harus disetujui mayoritas node, itulah sebabnya jumlah node dibuat ganjil. Model ini memberi ketersediaan tulis lebih baik, tetapi penanganan konfliknya lebih rumit.</p>

### Docker dan Docker Compose

<p align="justify">Docker mengemas aplikasi dan dependensinya menjadi image yang dijalankan sebagai container terisolasi, lebih ringan daripada mesin virtual karena berbagi kernel dengan host. Image bersifat immutable sehingga hasil praktikum bisa diulang. Docker Compose mendefinisikan banyak container dalam satu berkas YAML, dengan jaringan bersama sehingga service saling memanggil lewat nama, serta volume untuk menyimpan data. Perlu diingat bahwa depends_on hanya menunggu container dimulai, bukan layanannya siap, sehingga dibutuhkan loop until sebagai mekanisme tunggu.</p>

---


#  PEMBAHASAN
### 4.1 Streaming Replication Menggunakan PostgreSQL
### Install Docker
- Langkah-langkah Instal Docker 

<img width="402" height="290" alt="01" src="https://github.com/user-attachments/assets/4405358d-e059-4042-8329-da70aacbdf25" />

#### Pembahasan

<p align="justify">Pada tahap awal, installer Docker Desktop meminta pengguna menentukan mode instalasi. Opsi yang dipilih adalah Per-user installation dengan backend WSL 2, yaitu opsi yang direkomendasikan karena hanya memasang Docker untuk pengguna saat ini dan tidak memerlukan hak administrator. Opsi All-users installation tidak dipilih, padahal opsi itu diperlukan bila ingin memakai Windows Containers atau backend Hyper-V. Opsi Add shortcut to desktop juga dicentang agar Docker mudah dibuka dari desktop, lalu konfigurasi dilanjutkan dengan menekan tombol OK.</p>

- Proses Unpacking Files
  
<img width="527" height="364" alt="02" src="https://github.com/user-attachments/assets/27fd860d-5c9d-455b-9fe5-1c747adb7f8c" />

#### Pembahasan

<p align="justify">Setelah konfigurasi disetujui, installer Docker Desktop versi 4.97.0 mulai mengekstrak berkas-berkas program ke dalam sistem. Status “Unpacking files...” dan progress bar hijau yang baru terisi sedikit menunjukkan bahwa proses instalasi baru berjalan di tahap awal. Pada tahap ini pengguna hanya perlu menunggu sampai seluruh berkas selesai diekstrak.</p>

- Instalasi Berhasil

<img width="531" height="362" alt="03" src="https://github.com/user-attachments/assets/8f29d8d0-75e8-414c-b127-1d5160daa9fa" />

#### Pembahasan

<p align="justify">Tahap terakhir menampilkan pesan “Installation succeeded” dengan progress bar yang sudah penuh, yang berarti Docker Desktop 4.97.0 berhasil terpasang tanpa kendala. Pengguna cukup menekan tombol Close untuk menutup installer. Setelah itu Docker Desktop dapat dijalankan dan digunakan sebagai lingkungan praktikum, termasuk untuk menjalankan Docker Compose pada konfigurasi PostgreSQL dan Apache Ignite.</p>

---
### Pemeriksaan Versi dan Lingkungan
- versi Docker & Compose
#### Docker Version

<img width="270" height="35" alt="04" src="https://github.com/user-attachments/assets/f66b43ae-4b7d-4654-8bdc-181f1f9cb8e9" />

#### Pembahasan

<p align="justify">Perintah docker --version menampilkan Docker versi 29.9.2 (build a82e528). Ini membuktikan bahwa Docker CLI sudah terpasang dan dapat dikenali dari Command Prompt.</p>

#### Docker Compose Version

<img width="258" height="40" alt="05" src="https://github.com/user-attachments/assets/6e7f19c9-02e5-49bc-bb2c-87b4c9a118a1" />

#### Pembahasan

<p align="justify">Perintah docker compose version menampilkan Docker Compose v5.6.1. Hasil ini menunjukkan bahwa Compose sudah tersedia sebagai plugin Docker, sehingga berkas docker-compose.yaml pada proyek dapat dijalankan.</p>

#### Docker info

#### Cek info Docker

```python
docker info
```

#### Pembahasan

<p align="justify">Perintah docker info dipakai untuk menampilkan informasi sistem Docker, yang terdiri dari bagian Client dan bagian Server (Docker Engine). Pada gambar, bagian Client tampil dengan baik: Docker versi 29.9.2 dengan context desktop-linux, mode debug nonaktif, serta daftar plugin terpasang, di antaranya Docker Compose v5.6.1, Buildx v0.38.1, dan Docker Desktop commands v4.97.0. Hal ini menunjukkan bahwa instalasi Docker Desktop sudah lengkap dan sisi client siap digunakan.</p>

---

### Struktur Direktori dan FIle

<img width="218" height="92" alt="07" src="https://github.com/user-attachments/assets/6705cff0-522f-485f-a9c8-58871c50c0fe" />

#### Pembahasan

<p align="justify">Panel Explorer menampilkan folder streaming-replication yang berisi tiga berkas: 00_init.sql, docker-compose.yaml, dan env.sh. Berkas docker-compose.yaml mendefinisikan container primary dan replica, 00_init.sql berisi skrip SQL inisialisasi basis data, dan env.sh menyimpan variabel lingkungan yang dipakai saat konfigurasi. Struktur ini menjadi dasar proyek replikasi PostgreSQL pada praktikum.</p>


#### - 00_init.sql

<img width="511" height="73" alt="08" src="https://github.com/user-attachments/assets/f5ef0a01-1a43-4486-a585-0d2bafb82daa" />

#### Pembahasan

#### - docker-compose.yaml

<img width="422" height="398" alt="09" src="https://github.com/user-attachments/assets/37a592bf-39e9-4726-9b61-36cfd1149b69" />

#### Pembahasan

#### - env.sh

<img width="419" height="122" alt="10" src="https://github.com/user-attachments/assets/a5416c74-3505-46d0-a406-f8adb1ccebb3" />

#### Pembahasan

### Jalankan program menggunakan Docker

#### Periksa Docker
```python
docker --version
docker compose version
```

<img width="544" height="75" alt="11_Periksa_Docker" src="https://github.com/user-attachments/assets/6b326031-51a5-450e-80da-e4a34c69ac78" />

#### Pembahasan


#### Jalankan primary dan replica
```python
docker compose up -d
```

<img width="536" height="58" alt="12_Primary_dan_Replika" src="https://github.com/user-attachments/assets/721301bc-31d3-4ac2-984c-90868e278b20" />

#### Pembahasan

#### Periksa container
```python
docker ps
```

<img width="696" height="74" alt="13_Periksa_container" src="https://github.com/user-attachments/assets/9981bd55-cf06-4c65-bd7a-8b85a45c67dd" />

#### Pembahasan

#### Periksa log jika terjadi masalah
```python
docker compose logs postgres_primary
```

<img width="694" height="419" alt="14_Mengecek_Masalah" src="https://github.com/user-attachments/assets/1a525db7-3e37-457b-bd1c-23adb55cdbb3" />

#### Pembahasan

```python
docker compose logs postgres_replica
```

<img width="694" height="269" alt="15__Mengecek_Masalah" src="https://github.com/user-attachments/assets/975c01c2-2063-4974-a18d-0f32d48b326f" />
<img width="700" height="212" alt="16_Mengecek_Masalah" src="https://github.com/user-attachments/assets/219ee9fa-a3ba-4f6b-bcdf-3c63bcf4dbb0" />


#### Pembahasan

#### - Jalankan kode dibawah jika ingin menghentikan container
```python
docker compose down
```

<img width="545" height="67" alt="17_Menghentikan_container" src="https://github.com/user-attachments/assets/299f38b8-9e31-440e-92c6-83b59aebf62f" />

#### Pembahasan

### Pengujian Replikasi

<img width="959" height="415" alt="18" src="https://github.com/user-attachments/assets/84c6e1bd-1e4d-4c83-a73f-8e17649a4283" />

<img width="401" height="362" alt="19" src="https://github.com/user-attachments/assets/a4170f29-2951-4aa1-9964-b2daafb96441" />

#### Pembahasan

- Untuk melihat status pada server replica

<img width="463" height="218" alt="20" src="https://github.com/user-attachments/assets/e6fa772c-b933-4bdd-a7a6-a291e25a5fff" />

#### Pembahasan

-Primary

<img width="452" height="113" alt="21_Primary" src="https://github.com/user-attachments/assets/825b140b-60cb-4db5-8d69-f15fdc891017" />

#### Pembahasan

-Replica

<img width="451" height="140" alt="22_Replica" src="https://github.com/user-attachments/assets/6f3411d3-2717-4aed-b970-80282a141a5a" />

#### Pembahasan

#### Memanipulasi Data Primary

<img width="456" height="298" alt="23_data_Primary" src="https://github.com/user-attachments/assets/2bd5a7ea-d910-4282-9846-d18a77358ff2" />

#### Pembahasan

<img width="539" height="317" alt="24_data_Replica" src="https://github.com/user-attachments/assets/7b71427b-0547-40a2-9e55-0269e15861bc" />

#### Pembahasan

### High-Availability
#### Primary server mati

<img width="475" height="79" alt="25_Primary_Server_Stop" src="https://github.com/user-attachments/assets/8ba76c6b-fecb-4a1b-907b-628583345120" />

#### Pembahasan
<p align="justify">Perintah docker compose stop postgres_primary berhasil dijalankan, ditandai dengan status container streaming-replication-postgres_primary-1 yang berubah menjadi Stopped dalam waktu 0,9 detik. Dalam skenario praktikum streaming replication PostgreSQL, langkah ini mensimulasikan kegagalan (failover) pada node primary, sehingga server utama tidak lagi dapat melayani koneksi maupun menerima operasi tulis. Setelah primary mati, node replica (standby) tetap berjalan dan masih dapat melayani query baca, tetapi tidak bisa menerima penulisan karena masih berstatus read-only dan tidak lagi menerima aliran WAL dari primary. Langkah berikutnya yang umum dilakukan adalah mempromosikan replica menjadi primary baru, misalnya dengan pg_ctl promote atau SELECT pg_promote();, lalu memverifikasi bahwa node tersebut sudah keluar dari mode recovery (SELECT pg_is_in_recovery(); bernilai false) dan dapat menerima operasi tulis.</p>

Setelah memastikan bahwa server primary berada dalam kondisi mati (down), langkah selanjutnya adalah mengangkat replica menjadi primary baru dengan menjalankan fungsi pg_promote():

<img width="457" height="293" alt="26_Pg_Promote" src="https://github.com/user-attachments/assets/a87b70c3-983a-4fd6-ab00-74ddebfd88e6" />

#### Pembahasan

#### mematikan semua primary dan replika

<img width="466" height="166" alt="27_Docker_Compose_Down" src="https://github.com/user-attachments/assets/d254b4fb-13fa-45dc-87dc-c0fd8e78949f" />

#### Pembahasan


### 4.2 Replikasi Master-Master Menggunakan Apache Ignite 3

#### Struktur Direktori dan File

<img width="131" height="191" alt="28_Direktori_dan_file" src="https://github.com/user-attachments/assets/e53b62ad-06e1-4c25-88a1-7a55e31765b4" />

#### Pembahasan

<p align="justify">Selanjutnya, dibuat sebuah file bernama env.sh yang berfungsi sebagai shortcut (pintasan) dan berisi perintah-perintah berikut:</p>

<img width="620" height="78" alt="29_env sh" src="https://github.com/user-attachments/assets/04e078f6-706d-4d16-9ec0-4a3ddb5c8d5d" />

#### Pembahasan

####  Docker Compose

<img width="518" height="78" alt="30_tiga_node" src="https://github.com/user-attachments/assets/357829c8-b157-4895-ae8c-e2b6b381249d" />

#### Pembahasan

Setelah proses pull image selesai dan docker compose up berhasil dijalankan, status container akan ditampilkan sebagai berikut:

<img width="692" height="86" alt="31_Status_node" src="https://github.com/user-attachments/assets/63e661cd-c8c5-4ed6-a15b-78095a67b72b" />

#### Pembahasan

Setiap container yang berjalan di dalam network Docker memiliki IP internal. Untuk mengecek IP dari masing-masing node:

```python
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ignite3-node1-1
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ignite3-node2-1
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ignite3-node3-1
```

<img width="689" height="90" alt="32_alamat_IP_node" src="https://github.com/user-attachments/assets/20535869-2b35-4c93-a876-0c06d7b25997" />

#### Pembahasan

#### Inisialisasi Cluster

```python
docker run --rm -it --network=host -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 apacheignite/ignite:3.1.0 cli
```

<img width="692" height="221" alt="33_apache_ignite_CLI" src="https://github.com/user-attachments/assets/3dcddd97-3b99-42e5-9910-3aee0625e26d" />

#### Pembahasan

<p align="justify">CLI Apache Ignite 3 dijalankan lewat Docker dengan perintah docker run --rm -it --network=host ... apacheignite/ignite:3.1.0 cli, di mana --rm menghapus container otomatis setelah selesai dan --network=host memungkinkan akses ke node melalui localhost. CLI kemudian terhubung ke node default http://localhost:10300, namun muncul pemberitahuan bahwa cluster belum diinisialisasi, sehingga perlu menjalankan perintah cluster init terlebih dahulu.</p>

Selanjutnya, cluster diinisialisasi dengan menjalankan perintah berikut, kemudian status cluster diperiksa menggunakan perintah:

```python
cluster init --name=ignite3 --metastorage-group=node1,node2,node3
```

```python
cluster init --name=ignite3 --metastorage-group=node1,node2,node3
```

<img width="434" height="49" alt="34_inisialisasi_cluster_dan_status_cluster" src="https://github.com/user-attachments/assets/91cddc97-7caa-4e1a-9f45-640de2f95e89" />

#### Pembahasan

<p align="justify">cluster Apache Ignite 3 diinisialisasi melalui CLI dengan perintah cluster init --name=ignite3 --metastorage-group=node1,node2,node3, dan sistem merespons dengan pesan Cluster was initialized successfully. Parameter --name memberi nama cluster (ignite3), sedangkan --metastorage-group menentukan node-node yang menyimpan metadata cluster, yaitu node1, node2, dan node3. Setelah itu, perintah cluster status menampilkan bahwa cluster bernama ignite3 memiliki 3 node dengan status active. Daftar cmgNodes (Cluster Management Group) dan msNodes (Metastorage) sama-sama berisi node1, node2, dan node3, yang berarti ketiga node berpartisipasi dalam pengelolaan cluster sekaligus penyimpanan metadata, sehingga cluster siap digunakan dan memiliki redundansi jika salah satu node mengalami gangguan.</p>

<p align="justify">apabila ingin masuk kembali ke CLI menggunakan perintah yang sama, proses inisialisasi cluster tidak perlu dilakukan lagi karena cluster sudah diinisialisasi sebelumnya.</p>

<img width="691" height="221" alt="35_CLI" src="https://github.com/user-attachments/assets/ddb87c3f-5604-4b95-85a4-c79e17cec0b1" />

#### Pembahasan

<p align="justify">CLI Apache Ignite 3 dijalankan kembali dengan perintah Docker yang sama seperti sebelumnya, lalu terhubung ke node default http://localhost:10300 setelah dijawab Y. Berbeda dengan percobaan pertama, kali ini tidak muncul pesan bahwa cluster belum diinisialisasi, yang menandakan cluster sudah terinisialisasi dan siap digunakan. Dengan demikian, perintah cluster init tidak perlu dijalankan lagi, dan pengguna dapat langsung melanjutkan ke operasi berikutnya melalui prompt [node1]>.</p>

### Eksekusi Perintah SQL
#### Memuat dan Mengeksekusi File Skema SQL

```python
sql --file=/opt/ignite/sql/schema.sql
```

<img width="647" height="350" alt="36_Berkas_schema sql" src="https://github.com/user-attachments/assets/fc40da04-036a-4601-99ca-3315aeecc02b" />

#### Pembahasan

<p align="justify">CLI Apache Ignite 3 dijalankan dengan perintah Docker yang berbeda, yaitu menggunakan --network=ignite3_default agar container CLI berada di jaringan yang sama dengan ketiga node, serta --mount (bind) untuk memasang folder sql dari host ke /opt/ignite/downloads dalam mode readonly sehingga file SQL dapat diakses dari dalam container. Karena tidak lagi memakai jaringan host, koneksi ke node default http://localhost:10300 gagal dan muncul pesan Node unavailable. Hal ini diatasi dengan menghubungkan CLI secara manual menggunakan nama service Docker melalui perintah connect http://node1:10300, yang berhasil. Setelah itu, perintah sql --file=/opt/ignite/downloads/schema.sql dijalankan untuk mengeksekusi skrip skema, dan setiap pernyataan menampilkan Updated 0 rows. Pesan tersebut normal untuk perintah DDL seperti CREATE TABLE karena tidak ada baris data yang diubah, sehingga menandakan skema berhasil dibuat.</p>

---
Masukkan Kode berikut:

```python
sql
```
Lalu Kode berikut

```python
SELECT * FROM system.tables WHERE schema = 'PUBLIC';
```

<img width="599" height="179" alt="37_Schema_table_node1" src="https://github.com/user-attachments/assets/b534ec44-2e06-4f28-af1c-570b96db4172" />

#### Pembahasan

<p align="justify">perintah SELECT * FROM system.tables WHERE schema = 'PUBLIC'; dijalankan melalui sql-cli untuk menampilkan daftar tabel pada schema PUBLIC, dan hasilnya memperlihatkan 11 tabel dari dataset Chinook, yaitu ALBUM, PLAYLISTTRACK, TRACK, CUSTOMER, MEDIATYPE, PLAYLIST, ARTIST, INVOICELINE, EMPLOYEE, GENRE, dan INVOICE. Kolom ZONE_NAME menunjukkan bahwa sebagian besar tabel berada pada zona CHINOOK (zone ID 20), sedangkan tabel MEDIATYPE dan GENRE berada pada zona CHINOOKREPLICATED (zone ID 21), yang menandakan keduanya merupakan tabel referensi berukuran kecil yang direplikasi ke seluruh node. Kolom TABLE_COLOCATION_COLUMNS memperlihatkan strategi colocation, misalnya tabel TRACK dikelompokkan berdasarkan ALBUMID, ALBUM berdasarkan ARTISTID, dan INVOICE berdasarkan CUSTOMERID, sehingga data yang saling berelasi disimpan pada node yang sama untuk mengurangi transfer data antar-node saat operasi join. Dengan demikian, hasil ini mengonfirmasi bahwa skema dari schema.sql telah berhasil dibuat beserta pengaturan zona dan colocation-nya.</p>

<img width="218" height="281" alt="38_berkas_SQL" src="https://github.com/user-attachments/assets/5f7a84ed-4e83-42c6-8c9f-ce427ed25d27" />

#### Pembahasan

<p align="justify">CLI yang awalnya terhubung ke http://node1:10300 dipindahkan ke node kedua dengan perintah connect http://node2:10300. Sistem meminta konfirmasi karena CLI sudah terhubung ke node1, lalu dijawab Y dan koneksi ke node2 berhasil. Langkah ini dipakai untuk memeriksa apakah perubahan di node1 sudah terpropagasi ke node lain.</p>

---

### Verifikasi Propagasi Data

<p align="justify">Untuk memastikan bahwa perubahan yang dilakukan pada http://localhost:10300 telah dipropagasi ke node-node lainnya, dapat dilakukan pengecekan dengan menghubungkan CLI ke node yang berbeda. Berikut adalah koneksi ke node kedua di http://localhost:10301:</p>

```python
connect http://localhost:10301
```

<img width="363" height="25" alt="39_koneksi_CLI" src="https://github.com/user-attachments/assets/113d7786-da73-4000-8ebb-64784fc05cbb" />

#### Pembahasan

<p align="justify">Beberapa file SQL dijalankan berurutan untuk mengisi data dataset Chinook, yaitu current_catalog.sql, media_and_genre.sql, tracks.sql, ee_and_cust.sql, dan invoices.sql. Eksekusi tracks.sql pertama kali gagal dengan pesan File not found karena path /opt/ignite/sql/ salah, lalu berhasil setelah diganti ke /opt/ignite/downloads/ sesuai lokasi mount. Pesan Updated N rows menunjukkan jumlah baris yang berhasil dimasukkan, dan data dimasukkan dalam beberapa batch (misalnya 1000, 1000, 1000, 503 baris) sehingga seluruh tabel kini terisi.</p>

---

Cek Table

```python
SELECT * FROM system.tables WHERE schema = 'PUBLIC';
```

<img width="710" height="396" alt="40_table_node2" src="https://github.com/user-attachments/assets/24a8ac1f-06da-4c86-af35-95aacd858dec" />

#### Pembahasan

<p align="justify">setelah berpindah ke [node2], perintah SELECT * FROM system.tables WHERE schema = 'PUBLIC'; dijalankan kembali dan menampilkan hasil yang identik dengan yang sebelumnya terlihat di node1, yaitu 11 tabel Chinook (ALBUM, PLAYLISTTRACK, TRACK, CUSTOMER, MEDIATYPE, PLAYLIST, ARTIST, INVOICELINE, EMPLOYEE, GENRE, dan INVOICE) lengkap dengan zona, ID, dan kolom colocation yang sama. Tabel MEDIATYPE dan GENRE tetap berada pada zona CHINOOKREPLICATED, sedangkan sisanya pada zona CHINOOK. Hal ini membuktikan bahwa skema yang dibuat melalui node1 telah terpropagasi ke node2, karena metadata cluster dikelola bersama oleh seluruh node dalam metastorage group, sehingga perubahan di satu node langsung dapat dilihat dari node lain.</p>

---

query analytics:

```python
SELECT
    CAST(EXTRACT(YEAR FROM i.InvoiceDate) AS VARCHAR) || '-' ||
    CASE
        WHEN EXTRACT(MONTH FROM i.InvoiceDate) < 10
        THEN '0' || CAST(EXTRACT(MONTH FROM i.InvoiceDate) AS VARCHAR)
        ELSE CAST(EXTRACT(MONTH FROM i.InvoiceDate) AS VARCHAR)
    END AS YearMonth,
    COUNT(DISTINCT i.InvoiceId) AS InvoiceCount,
    COUNT(DISTINCT i.CustomerId) AS CustomerCount,
    SUM(i.Total) AS MonthlyRevenue,
    AVG(i.Total) AS AverageOrderValue
FROM
    Invoice i
GROUP BY
    EXTRACT(YEAR FROM i.InvoiceDate), EXTRACT(MONTH FROM i.InvoiceDate)
ORDER BY
    YearMonth DESC;
```

<img width="257" height="425" alt="41_query_analitik_node2" src="https://github.com/user-attachments/assets/eb8ac6d5-735f-4dfe-a915-426cc5c1543b" />

<img width="217" height="426" alt="42_query_analitik_node2" src="https://github.com/user-attachments/assets/f9582a1b-d1a6-4f78-90f5-24220e259083" />

#### Pembahasan

<p align="justify">dijalankan query agregasi pada tabel Invoice yang mengelompokkan data berdasarkan tahun dan bulan dari InvoiceDate, lalu mengurutkannya dari yang terbaru (ORDER BY YearMonth DESC). Kolom YearMonth dibentuk dengan menggabungkan hasil EXTRACT(YEAR ...) dan EXTRACT(MONTH ...) melalui CASE, di mana bulan di bawah 10 diberi awalan '0' agar formatnya seragam (misalnya 2024-09). Untuk setiap bulan, query menghitung InvoiceCount (jumlah invoice), CustomerCount (jumlah pelanggan unik), MonthlyRevenue (total pendapatan), dan AverageOrderValue (rata-rata nilai pesanan). Hasilnya mencakup periode Januari 2020 hingga Desember 2024, dengan sebagian besar bulan memiliki 7 invoice dari 7 pelanggan dan pendapatan sekitar 37,62. Beberapa bulan menyimpang, misalnya 2024-12 (38,62), 2024-11 (49,62), 2023-09 (46,71), dan 2022-06 (50,62) yang lebih tinggi, serta 2022-11 (23,76) yang paling rendah. Karena jumlah invoice sama dengan jumlah pelanggan unik di setiap bulan, tiap pelanggan rata-rata hanya melakukan satu transaksi per bulan.</p>

---

#### Menghentikan semua node
Matikan Node:

```python
Docker compose down
```

<img width="401" height="74" alt="43_Menghentikan_semua_node" src="https://github.com/user-attachments/assets/a63ea1d9-e990-4fb4-b58e-93e44d9cc908" />

#### Pembahasan

<p align="justify">perintah docker compose down dijalankan di folder proyek Apache Ignite untuk menghentikan dan menghapus seluruh resource yang dibuat oleh docker compose up. Ketiga container, yaitu ignite3-node1-1, ignite3-node3-1, dan ignite3-node2-1, berhasil dihapus (Removed). Namun, network ignite3_default menampilkan peringatan Resource is still in use sehingga belum bisa dihapus. Hal ini kemungkinan terjadi karena masih ada container lain yang terhubung ke network tersebut, misalnya container CLI yang dijalankan dengan --network=ignite3_default dan belum ditutup. Masalah ini dapat diatasi dengan keluar dari sesi CLI terlebih dahulu (container CLI otomatis terhapus berkat opsi --rm), lalu menjalankan docker compose down kembali agar network ikut dibersihkan.</p>



# KESIMPULAN

<p align="justify">Kedua praktikum ini menunjukkan bahwa replikasi bukanlah satu teknik tunggal, melainkan kumpulan keputusan desain yang masing-masing membawa konsekuensi. Pada PostgreSQL, streaming replication berhasil menjaga replica tetap sama dengan primary melalui aliran WAL: replica hanya bisa dibaca, mengikuti setiap perubahan secara otomatis, dan dapat dinaikkan menjadi primary ketika primary dihentikan. Meski begitu, kenaikan peran tersebut dilakukan secara manual, replikasinya bersifat asinkron, dan belum ada mekanisme yang mencegah split-brain, sehingga konfigurasi ini baru menyiapkan fondasi untuk High Availability dan belum bisa disebut High Availability yang utuh. Apache Ignite memperlihatkan pendekatan yang berbeda, yaitu tiga node yang kedudukannya sama, masing-masing bisa menerima baca dan tulis, dan perubahan di satu node langsung tampak di node lainnya tanpa proses promosi. Jika dibandingkan, primary-replica lebih sederhana dan mudah dipahami tetapi tetap bertumpu pada satu titik penulisan, sedangkan master-master lebih tahan ketika salah satu node gagal namun menuntut konfigurasi dan koordinasi yang lebih rumit. Karena itu, pemilihan modelnya tidak bergantung pada mana yang lebih baru, melainkan pada kebutuhan aplikasi: seberapa besar kehilangan data yang masih bisa diterima, seberapa berat beban tulisnya, dan seberapa siap tim mengelola kerumitannya.</p>

---
# REFERENSI

- PostgreSQL Global Development Group, "High Availability, Load Balancing, and Replication," *PostgreSQL 18 Documentation*, 2025. [Daring]. Tersedia: https://www.postgresql.org/docs/18/high-availability.html
- PostgreSQL Global Development Group, "Write-Ahead Logging (WAL)," *PostgreSQL 18 Documentation*, 2025. [Daring]. Tersedia: https://www.postgresql.org/docs/18/wal.html
- PostgreSQL Global Development Group, "pg_basebackup," *PostgreSQL 18 Documentation*, 2025. [Daring]. Tersedia: https://www.postgresql.org/docs/18/app-pgbasebackup.html
- Eremeykin, "How to Setup Single Primary PostgreSQL Replication with Docker Compose," *Medium*. [Daring]. Tersedia: https://medium.com/@eremeykin/how-to-setup-single-primary-postgresql-replication-with-docker-compose 98c48f233bbf
- Docker Inc., "Install Docker Engine dan Docker Compose," *Docker Documentation*, 2025. [Daring]. Tersedia: https://docs.docker.com/
- A. S. Tanenbaum dan M. van Steen, *Distributed Systems*, edisi ke-4. Maarten van Steen, 2023.
- M. Kleppmann, *Designing Data-Intensive Applications*. O'Reilly Media, 2017.
