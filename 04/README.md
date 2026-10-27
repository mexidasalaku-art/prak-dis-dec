# Praktikum Minggu MODUL 04 - Konsistensi dan Replikasi pada Sistem Terdistribusi

| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi |
| **Topik** | Konsistensi dan Replikasi pada Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 | 
| **Kelas** | IF-1 |

---

## Daftar Isi

1. [Tujuan Praktikum](#1-tujuan-praktikum)
2. [Ringkasan Konsep](#2-ringkasan-konsep)
3. [Struktur Repositori](#3-struktur-repositori)
4. [Bagian A: Persiapan Docker](#4-bagian-a-persiapan-docker)
5. [Bagian B: Streaming Replication PostgreSQL 18](#5-bagian-b-streaming-replication-postgresql-18-primary-replica)
6. [Bagian C: Replikasi Master-Master Apache Ignite 3](#6-bagian-c-replikasi-master-master-apache-ignite-3)
7. [Perbandingan Dua Model Replikasi](#7-perbandingan-dua-model-replikasi)
8. [Kesimpulan](#8-kesimpulan)
9. [Catatan dan Pemecahan Masalah](#9-catatan-dan-pemecahan-masalah)
10. [Referensi](#10-referensi)

---

##  Tujuan Praktikum

##  Dasar Teori
---

## 2. Ringkasan Konsep

### 2.1 Konsistensi dan Replikasi

Menyimpan data di satu mesin berarti seluruh layanan bergantung pada satu titik gagal. **Replikasi** menjaga salinan data di beberapa node sehingga:

- layanan tetap hidup saat satu node bermasalah,
- pembacaan bisa dibagi ke beberapa node,
- data bisa diletakkan lebih dekat ke pengguna.

Konsekuensinya, setiap salinan harus diperbarui dan muncul pertanyaan: *kapan sebuah salinan boleh dianggap sama dengan yang lain?* Itulah inti **konsistensi**.

| Model | Jaminan | Biaya |
|---|---|---|
| **Konsistensi kuat** | Setiap pembacaan melihat tulisan terakhir yang selesai | Tulis harus menunggu koordinasi antar node (lambat) |
| **Konsistensi eventual** | Salinan boleh tertinggal sesaat, tetapi akhirnya konvergen | Pembaca bisa melihat data lama |
| **Kausal / read-your-writes** | Sebagian jaminan yang paling dibutuhkan aplikasi | Menengah |

**Teorema CAP:** saat terjadi pemisahan jaringan, sistem harus memilih antara tetap *konsisten* atau tetap *tersedia*. Dalam praktik, pilihan ini dibuat per operasi dan per kebutuhan, bukan sekali untuk seluruh sistem.

### 2.2 Primary-Replica dan Streaming Replication

Pada model **primary-replica**, satu node (primary) menerima semua tulisan, sedangkan replica menerima perubahan darinya dan biasanya melayani pembacaan. Tidak ada konflik tulis karena hanya ada satu penulis, dan replica menjadi calon pengganti saat primary gagal.

| | Sinkron | Asinkron |
|---|---|---|
| Commit | Menunggu konfirmasi replica | Langsung commit, kirim di belakang |
| Risiko kehilangan data saat failover | Bisa nol | Ada jendela kecil data belum sampai |
| Latensi tulis | Naik | Tetap cepat |
| Ketergantungan primary pada replica | Ya | Tidak |

**Streaming replication** berarti perubahan dialirkan terus-menerus begitu terjadi (bukan snapshot berkala). PostgreSQL melakukannya dengan mengalirkan WAL dari proses *walsender* di primary ke *walreceiver* di replica.

### 2.3 WAL, LSN, dan Replication Slot

- **WAL (Write-Ahead Log):** catatan berurutan setiap perubahan; perubahan ditulis ke WAL **sebelum** halaman data diperbarui. Awalnya untuk pemulihan crash, tetapi aliran WAL yang sama bisa diputar ulang di replica sehingga hasilnya identik dengan primary.
- **LSN (Log Sequence Number):** penanda posisi di WAL. Selisih posisi kirim, tulis, flush, dan replay disebut **lag replikasi**.
- **Replication slot:** penanda di sisi server yang menjamin WAL ditahan sampai replica mengonfirmasi. Risikonya: jika replica mati lama, WAL menumpuk dan bisa menghabiskan disk.
- **`hot_standby_feedback`:** memberi tahu primary tentang query yang sedang berjalan di replica agar baris yang masih dibutuhkan tidak dibersihkan terlalu cepat.

### 2.4 High Availability, Failover, dan Split-Brain

- **RTO** = lama downtime yang dapat diterima; **RPO** = jumlah data yang boleh hilang.
- **Failover** = memindahkan peran primary ke replica. Bisa manual (`pg_promote()`) atau otomatis dengan alat seperti Patroni / repmgr berbasis quorum.
- **Split-brain** = dua node sama-sama menganggap dirinya primary dan menerima tulisan, sehingga data bercabang. Pencegahannya adalah **fencing** (memastikan node lama benar-benar tidak bisa menulis).

> [!WARNING]
> Pada praktikum ini pencegahan split-brain dilakukan **manual**: primary lama dihentikan dan tidak dihidupkan lagi sebagai primary. Ini yang membedakan replikasi sederhana dari sistem HA yang siap produksi.

### 2.5 Apache Ignite 3 dan Master-Master

Apache Ignite 3 menyimpan data di memori dan disk. Data dipecah menjadi partisi berdasarkan *affinity key* lalu ditempatkan di node sesuai **zone**. Zone juga menentukan *replication factor*. Semua node terlihat setara: setiap node dapat menerima baca/tulis dan meneruskan permintaan ke node pemilik partisi.

Metadata cluster (daftar node, definisi zone) dikelola oleh *cluster management group* dengan **consensus**, sehingga butuh mayoritas node dan jumlah node ganjil. Pada dataset Chinook, tabel besar didistribusikan, sedangkan tabel referensi kecil (`MEDIATYPE`, `GENRE`) digandakan penuh ke semua node.

### 2.6 Docker sebagai Lingkungan Praktikum

- **Image** bersifat immutable, sehingga setiap container baru dimulai dari kondisi yang sama dan hasil praktikum dapat diulang.
- **Docker Compose** mendefinisikan beberapa container dalam satu YAML; service saling memanggil dengan nama service sebagai hostname (contoh: `postgres_primary`).
- **`healthcheck`** membuat status container bermakna (`healthy`), sedangkan **`depends_on`** hanya mengatur urutan start, **bukan** kesiapan layanan. Itulah sebabnya perintah backup replica dibungkus loop `until`.

---

## 3. Struktur Repositori

```text
.
├── README.md
├── assets/                       # tangkapan layar (gambar-4.1.png, dst.)
├── streaming-replication/        # Bagian B: PostgreSQL
│   ├── 00_init.sql
│   ├── docker-compose.yaml
│   └── env.sh
└── src--ApacheIgnite/            # Bagian C: Apache Ignite
    ├── sql/
    │   ├── schema.sql
    │   ├── current_catalog.sql
    │   ├── media_and_genre.sql
    │   ├── ee_and_cust.sql
    │   ├── tracks.sql
    │   └── invoices.sql
    ├── docker-compose.yaml
    └── env.sh
```

---

## 4. Bagian A: Persiapan Docker

### 4.1 Instalasi Docker Desktop (Windows)

| Langkah | Keterangan |
|---|---|
| Konfigurasi | Pilih **Per-user installation**: tidak butuh hak administrator dan otomatis memakai backend **WSL 2** (wajib untuk container Linux). Biarkan *Add shortcut to desktop* tercentang. |
| Ekstraksi | Jangan tutup installer sebelum progress bar penuh; komponen yang tertinggal sering membuat Docker gagal start. |
| Selesai | Pesan *Installation succeeded* hanya berarti berkas terpasang. Buka Docker Desktop dan tunggu status **Engine running**. |

![Konfigurasi instalasi](assets/gambar-4.1.png)
![Ekstraksi berkas](assets/gambar-4.2.png)
![Instalasi berhasil](assets/gambar-4.3.png)

> [!TIP]
> Jika perintah `docker` mengembalikan error koneksi ke pipe, cukup tunggu engine selesai boot; tidak perlu menginstal ulang.

### 4.2 Verifikasi Versi

```bash
docker --version          # Docker version 29.9.2, build a82e528
docker compose version    # Docker Compose version v5.6.1
```

![docker --version](assets/gambar-4.4.png)
![docker compose version](assets/gambar-4.5.png)

Compose terpasang sebagai **plugin** (`docker compose`, dengan spasi), bukan `docker-compose` versi lama. Alias di `env.sh` memakai bentuk berspasi.

### 4.3 Memeriksa Engine

```bash
docker info
```

Ringkasan bagian **Server** pada mesin praktikum:

| Item | Nilai |
|---|---|
| Server Version | 29.9.2 |
| Containers | 0 |
| Storage Driver | overlayfs |
| Cgroup Version | 2 |
| Kernel | 6.18.33.2-microsoft-standard-WSL2 |
| CPU / Memori | 12 CPU / 7,606 GiB |

> [!IMPORTANT]
> Memori sekitar 7,6 GiB cukup untuk dua container PostgreSQL kecil, tetapi bisa menjadi kendala jika tiga node Ignite masing-masing meminta 4 GB. Jika bagian Server kosong/error, engine belum hidup.

---

## 5. Bagian B: Streaming Replication PostgreSQL 18 (Primary-Replica)

### 5.1 Berkas yang Dibutuhkan

![Struktur direktori](assets/gambar-4.6.png)

| Berkas | Peran | Kapan dibaca |
|---|---|---|
| `00_init.sql` | Membuat user replikasi dan slot | Sekali, saat volume data primary pertama dibuat |
| `docker-compose.yaml` | Mendefinisikan primary dan replica | Setiap `docker compose` dijalankan |
| `env.sh` | Alias perintah singkat | Hanya di sesi shell yang memuatnya |

> [!NOTE]
> Nama folder menjadi nama project Compose, sehingga container bernama `streaming-replication-postgres_primary-1` dan `streaming-replication-postgres_replica-1`.

#### `00_init.sql`

![Isi 00_init.sql](assets/gambar-4.7.png)

Dua baris saja, tetapi inilah yang membuat replikasi bisa jalan:

1. Membuat user **`replicator`** dengan hak `REPLICATION` (khusus untuk mengambil stream WAL, bukan untuk aplikasi).
2. Membuat **physical replication slot** `replication_slot` agar primary tidak membuang WAL yang belum dibaca replica, sehingga replica yang sempat mati bisa menyusul tanpa `pg_basebackup` dari nol.

> [!WARNING]
> File di `/docker-entrypoint-initdb.d` hanya dijalankan saat volume data pertama dibuat. Mengubah isinya kemudian tidak berefek sebelum data lama dihapus.

#### `docker-compose.yaml`

![Isi docker-compose.yaml](assets/gambar-4.8.png)

Konfigurasi bersama dipakai lewat *anchor* `x-postgres-common` (image `postgres:18.3-alpine3.23`, user `postgres`, `restart: always`, healthcheck `pg_isready`).

**Service primary** (port 5432, user `zuser`, database `zdb`) dengan parameter penting:

| Parameter | Alasan |
|---|---|
| `wal_level=replica` | WAL memuat informasi yang dibutuhkan standby |
| `hot_standby=on` | Replica dapat di-query |
| `max_wal_senders`, `max_replication_slots` | Menyediakan cukup koneksi dan slot replikasi |
| `hot_standby_feedback=on` | Query panjang di replica tidak membuat baris yang dibutuhkan terhapus di primary |

**Service replica** tidak menjalankan `initdb`. Ia menunggu `pg_basebackup` berhasil (loop `until`) dengan flag:

- `-X stream` : ikut mengalirkan WAL selama backup,
- `-R` : otomatis menulis `standby.signal` dan `primary_conninfo`, sehingga replica tidak perlu dikonfigurasi manual.

#### `env.sh`

![Isi env.sh](assets/gambar-4.9.png)

| Alias | Perintah |
|---|---|
| `dcu` | `docker compose up -d` |
| `dcd` | `docker compose down` |
| `dps` | `docker ps` |
| `dep` / `der` | `docker exec` ke primary / replica |
| `dlp` / `dlr` | `docker logs` primary / replica |

> [!NOTE]
> Nama container di dalam alias ditulis lengkap dan mengikuti nama folder. Jika folder diganti nama, alias harus disesuaikan. Versi ini tidak memakai `sudo` karena Docker Desktop di Windows sudah berjalan dengan hak akses memadai.

### 5.2 Menjalankan Cluster

```bash
cd 04/streaming-replication
ls -la              # pastikan 3 berkas ada dan tidak kosong
source env.sh       # memuat alias ke shell aktif
docker compose up -d   # atau: dcu
```

![ls -la](assets/gambar-4.10.png)
![source env.sh](assets/gambar-4.11.png)
![docker compose up -d](assets/gambar-4.12.png)
![Menjalankan ulang dengan dcu](assets/gambar-4.13.png)

**Hasil:** image `postgres:18.3-alpine3.23` diunduh (~33 detik), network `streaming-replication_default` dibuat, lalu kedua container dijalankan. Menjalankan `dcu` kedua kali hanya menampilkan `Running`: Compose bersifat **idempoten**.

> [!TIP]
> `source env.sh` harus diulang di setiap terminal baru dan dijalankan dari folder yang benar. Menjalankan `./env.sh` tidak akan memuat alias ke shell aktif.

### 5.3 Memeriksa Status Container

```bash
dps     # kedua container harus Up ... (healthy)
dlr     # log replica
```

![Status healthy](assets/gambar-4.14.png)
![Log replica](assets/gambar-4.15.png)

Alternatif tanpa alias: `docker logs streaming-replication-postgres_replica-1`.

**Membaca log replica** (satu log menceritakan seluruh siklus):

| Cuplikan log | Arti |
|---|---|
| `pg_basebackup: error: ... Connection refused` lalu `Retrying in 5 seconds ...` | Replica start lebih dulu daripada primary siap; `depends_on` tidak menunggu kesiapan layanan. Bukan kegagalan permanen. |
| `Backup done, starting replica...` | `pg_basebackup` akhirnya berhasil |
| `entering standby mode` → `consistent recovery state reached` → `ready to accept read-only connections` | Replica menyala sebagai standby yang dapat dibaca |
| `started streaming WAL from primary at 0/3000000 on timeline 1` | **Tanda replikasi sudah berjalan** |
| `replication terminated by primary server` → `waiting for WAL to become available` | Primary dimatikan (tahap HA); replica menunggu dan mencoba menyambung kembali |

### 5.4 Verifikasi Lewat Tabel Diagnostik

Masuk ke primary lalu buka `psql`:

```bash
dep
psql -U zuser -d zdb
```

```sql
\x
SELECT * FROM pg_stat_replication;
SELECT * FROM pg_replication_slots;
```

![pg_stat_replication](assets/gambar-4.16.png)
![pg_replication_slots](assets/gambar-4.17.png)

| Kolom | Nilai | Makna |
|---|---|---|
| `state` | `streaming` | Aliran WAL aktif |
| `application_name` | `walreceiver` | Koneksi dari replica |
| `client_addr` | `172.18.0.3` | Alamat replica |
| `sent_lsn` = `write_lsn` = `flush_lsn` = `replay_lsn` | `0/304F638` | **Tidak ada lag**: semua sudah dikirim, ditulis, di-flush, dan diputar ulang |
| `sync_state` | `async` | Replikasi **asinkron** |
| Slot `replication_slot` | `physical`, `active = t` | Slot terpakai |
| `wal_status` | `reserved` | WAL masih ditahan |

Di replica:

```bash
der
psql -U zuser -d zdb
```

```sql
SELECT pg_is_in_recovery();   -- t
```

![pg_is_in_recovery](assets/gambar-4.18.png)

Nilai `t` berarti node ini standby yang sedang memutar ulang WAL: **dapat dibaca, tetapi menolak tulisan**.

### 5.5 Uji Replikasi Data

**Langkah 1: baseline (sebelum ada tabel).** `\dt` di primary dan replica sama-sama menghasilkan `Did not find any tables.` Ini berfungsi sebagai kontrol percobaan: satu-satunya sumber perubahan nanti adalah perintah di primary.

![Primary sebelum tabel](assets/gambar-4.19.png)
![Replica sebelum tabel](assets/gambar-4.20.png)

**Langkah 2: tulis data di primary.**

```sql
CREATE TABLE testrep (first INT, second VARCHAR(15));
SELECT * FROM testrep;
INSERT INTO testrep VALUES (21, 'Test pertama');
INSERT INTO testrep VALUES (23, 'Test ke dua');
SELECT * FROM testrep;
```

![Manipulasi data di primary](assets/gambar-4.21.png)

> [!NOTE]
> Tanpa `BEGIN`/`COMMIT`, tiap perintah berjalan dalam transaksi implisit dan langsung di-commit. Ini penting: WAL hanya memuat transaksi yang sudah commit, sehingga transaksi menggantung tidak akan pernah sampai ke replica.

**Langkah 3: baca di replica.**

```sql
\dt
SELECT * FROM testrep;
```

![Data muncul di replica](assets/gambar-4.22.png)

`\dt` pertama masih kosong, tetapi `\dt` beberapa saat kemudian sudah menampilkan `testrep` dengan dua baris yang sama persis. Jeda sepersekian detik ini adalah **demonstrasi nyata konsistensi eventual** pada replikasi asinkron. Tidak ada satu pun perintah tulis dijalankan di replica; semuanya berasal dari replay WAL.

### 5.6 Skenario High Availability: Failover Manual

**Langkah 1: matikan primary.**

```bash
docker-compose stop postgres_primary
```

![Primary dihentikan](assets/gambar-4.23.png)

Replica tidak ikut mati, tetapi koneksi streaming terputus. Replica masih melayani pembacaan data yang ia miliki, namun **tidak ada node yang menerima tulisan**.

**Langkah 2: promosikan replica.**

```sql
SELECT pg_is_in_recovery();   -- t
SELECT pg_promote();          -- t (perintah diterima)
SELECT pg_is_in_recovery();   -- f (sudah menjadi primary)
```

![pg_promote](assets/gambar-4.24.png)

Perubahan `t` → `f` berarti PostgreSQL berhenti memutar ulang WAL, menghapus penanda standby, dan membuka akses read-write.

> [!CAUTION]
> **Konsekuensi failover manual asinkron:**
> 1. Transaksi terakhir di primary yang belum sempat sampai ke replica **bisa hilang**.
> 2. Jika primary lama dihidupkan lagi dan masih menganggap dirinya primary, terjadi **split-brain** (data bercabang). Penanganannya butuh `pg_rewind` atau pembangunan ulang replica, bukan sekadar menyalakan container.

### 5.7 Membersihkan Lingkungan

```bash
dcd    # docker compose down
dps    # kosong
```

![docker compose down](assets/gambar-4.25.png)

Tiga resource dihapus: container replica, container primary, dan network `streaming-replication_default`.

| Perintah | Efek |
|---|---|
| `docker compose stop` | Menghentikan container, masih bisa di-`start` lagi |
| `docker compose down` | Menghapus container **dan** network |

Karena tidak ada *named volume*, data PostgreSQL ikut hilang; `up` berikutnya menjalankan `initdb` dan `pg_basebackup` dari awal. Tambahkan volume eksplisit jika data harus bertahan.

---

## 6. Bagian C: Replikasi Master-Master Apache Ignite 3

### 6.1 Berkas yang Dibutuhkan

![Struktur direktori Ignite](assets/gambar-4.26.png)

Berkas SQL berasal dari paket `sql.zip` pada dokumentasi quick start Apache Ignite 3 (dataset **Chinook**), diekstrak ke folder `sql/`. Seluruh `docker-compose.yaml` dan SQL bersumber dari <https://ignite.apache.org/docs/ignite3/latest/quick-start/explore-sql>.

| Berkas SQL | Fungsi |
|---|---|
| `schema.sql` | Membuat tabel (DDL) |
| `current_catalog.sql`, `tracks.sql`, `media_and_genre.sql`, `ee_and_cust.sql`, `invoices.sql` | Mengisi data |

#### `env.sh` untuk Ignite

![env.sh Ignite](assets/gambar-4.27.png)

Selain alias seperti pada Bagian B, ada dua alias CLI:

| Alias | Fungsi |
|---|---|
| `dclm` | Menjalankan CLI dengan folder `sql` di-**mount** ke `/opt/ignite/sql` |
| `dcli` | Menjalankan CLI tanpa mount |

Keduanya memakai `--network=host` agar CLI dapat menjangkau `http://localhost:10300`. Pada `dclm` terdapat `MSYS_NO_PATHCONV=1` (khas **Git Bash di Windows**) agar path `./sql:/opt/ignite/sql` tidak diterjemahkan ulang menjadi path Windows sehingga mount gagal.

### 6.2 Menjalankan Cluster

```bash
source env.sh
dcu
dps
```

![Menjalankan Compose](assets/gambar-4.28.png)
![Status tiga node](assets/gambar-4.29.png)

- Image `apacheignite/ignite:3.1.0` diunduh (~56 detik), network `ignite3_default` dibuat, tiga container jalan: `ignite3-node1-1`, `ignite3-node2-1`, `ignite3-node3-1`.
- Nama `ignite3` berasal dari `name: ignite3` di dalam file compose (bukan nama folder).
- Ketiganya memakai anchor `x-ignite-def`; yang berbeda hanya `--node-name` dan port.
- `nodeFinder.netClusterNodes` menyebut ketiga node pada port **3344** agar saling menemukan.
- Tidak ada `healthcheck`, sehingga status hanya `Up` (tanpa `healthy`).

| Node | REST API / CLI | Port aplikasi |
|---|---|---|
| node1 | 10300 | 10800 |
| node2 | 10301 | 10801 |
| node3 | 10302 | 10802 |

**Memeriksa IP internal node:**

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ignite3-node1-1
```

![IP internal node](assets/gambar-4.30.png)

| Node | IP |
|---|---|
| node1 | 172.18.0.3 |
| node2 | 172.18.0.2 |
| node3 | 172.18.0.4 |

> [!WARNING]
> IP container bisa berubah saat network dibuat ulang. Gunakan nama service (`node1`, `node2`) dan jangan di-*hardcode* di aplikasi.

### 6.3 Inisialisasi Cluster

```bash
dcli
# atau:
docker run --rm -it --network=host -e LANG=C.UTF-8 -e LC_ALL=C.UTF-8 apacheignite/ignite:3.1.0 cli
```

Jawab `Y` saat ditanya koneksi ke node default `http://localhost:10300`; prompt berubah menjadi `[node1]`.

![CLI terhubung](assets/gambar-4.31.png)

```text
cluster init --name=ignite3 --metastorage-group=node1,node2,node3
```

![Inisialisasi cluster](assets/gambar-4.32.png)

Ketiga node dipilih sebagai *metastorage group* karena metadata dikelola dengan **consensus**; jumlah ganjil membuat pemilihan pemimpin tetap bisa berjalan jika satu node bermasalah. Perintah ini hanya boleh dijalankan **sekali** (`Cluster was initialized successfully`).

```text
cluster status
```

![Status cluster](assets/gambar-4.33.png)

```text
[name: ignite3, nodes: 3, status: active, cmgNodes: [node1, node2, node3], msNodes: [node1, node2, node3]]
```

`status: active` dan `nodes: 3` membuktikan ketiga container benar-benar satu cluster, bukan sekadar tiga proses yang kebetulan hidup.

Masuk ulang ke CLI tidak memerlukan inisialisasi lagi (metadata dibaca dari metastorage):

![Masuk ulang CLI](assets/gambar-4.34.png)

> [!NOTE]
> Karena tidak ada volume permanen, metadata hanya bertahan selama container hidup. Setelah `down`, cluster harus diinisialisasi lagi.

### 6.4 Memuat Skema dan Data

```text
sql --file=/opt/ignite/sql/schema.sql
```

![Eksekusi schema.sql](assets/gambar-4.35.png)

Output `Updated 0 rows.` berulang itu **wajar** karena isinya DDL (`CREATE TABLE`). Yang perlu dipastikan hanyalah tidak ada pesan error.

Masuk ke mode SQL dan cek tabel:

```text
sql
SELECT * FROM system.tables WHERE schema = 'PUBLIC';
```

![Daftar tabel PUBLIC](assets/gambar-4.36.png)
![Eksekusi berkas data](assets/gambar-4.37.png)

Hasilnya 11 tabel: `ALBUM`, `PLAYLISTTRACK`, `TRACK`, `CUSTOMER`, `MEDIATYPE`, `PLAYLIST`, `ARTIST`, `INVOICELINE`, `EMPLOYEE`, `GENRE`, `INVOICE`.

| Zone | Tabel | Perilaku |
|---|---|---|
| `CHINOOK` | Sebagian besar tabel | Data **didistribusikan** per partisi ke node tertentu |
| `CHINOOKREPLICATED` | `MEDIATYPE`, `GENRE` | Seluruh isi tabel **digandakan ke semua node** (data referensi kecil dan sering di-join) |

Jumlah baris yang dilaporkan saat memuat data:

| Berkas | Baris diubah |
|---|---|
| `current_catalog.sql` | 275, 347 |
| `media_and_genre.sql` | 25, 5 |
| `tracks.sql` | 1000, 1000, 1000, 503 |
| `ee_and_cust.sql` | 8, 59 |
| `invoices.sql` | 412, 240, 18, 715, dan beberapa blok 1000 |

### 6.5 Verifikasi Propagasi ke Node Lain

Membaca dari node yang sama tempat data ditulis tidak membuktikan replikasi, maka koneksi dipindah ke node lain:

```text
connect http://localhost:10301
```

![Pindah ke node2](assets/gambar-4.38.png)

Jawab `Y`; prompt berubah menjadi `[node2]`. Lalu:

```sql
SELECT * FROM system.tables WHERE schema = 'PUBLIC';
```

![Tabel di node2](assets/gambar-4.39.png)

Daftar tabel, `ZONE_NAME`, dan `TABLE_ID` **identik** dengan node1: definisi skema dikelola cluster lewat consensus, jadi lapisan skema sudah konsisten di ketiga node.

**Query analitik** (dijalankan di node2, lalu node3):

```sql
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

![Analitik node2 (1)](assets/gambar-4.40.png)
![Analitik node2 (2)](assets/gambar-4.41.png)

Hasil mencakup **2020-01 s.d. 2024-12** dengan 6-7 invoice per bulan. Nilai `MonthlyRevenue` yang sering 37,62 dan `AverageOrderValue` ≈ 5,37 adalah karakter data contoh (kecil dan berulang); beberapa bulan seperti 2023-05 dan 2022-06 berbeda karena komposisi invoice-nya berbeda.

Pengecekan di node3 (`http://localhost:10302`):

![Analitik node3 (1)](assets/gambar-4.42.png)
![Analitik node3 (2)](assets/gambar-4.43.png)

Hasil node3 **sama persis** dengan node2 hingga digit desimal. Kesamaan ini bukan karena satu primary menyalin ke node lain, melainkan karena Ignite mendistribusikan dan mereplikasi data di tingkat partisi sendiri. Semua node melayani pembacaan dan dapat menerima penulisan, itulah arti master-master.

### 6.6 Menghentikan Cluster

```bash
dcd
```

![docker compose down Ignite](assets/gambar-4.44.png)

Empat resource dihapus: tiga container node dan network `ignite3_default`. Tanpa volume permanen, seluruh data dan metadata ikut hilang; pada praktikum berikutnya `cluster init` dan seluruh SQL harus dijalankan ulang. Ini pilihan desain agar lingkungan praktikum bersih setiap kali dijalankan.

---

## 7. Perbandingan Dua Model Replikasi

| Aspek | PostgreSQL (primary-replica) | Apache Ignite 3 (master-master) |
|---|---|---|
| Titik tulis | Satu (primary) | Setiap node |
| Peran replica | Read-only (`pg_is_in_recovery() = t`) | Tidak ada; semua node setara |
| Mekanisme sinkronisasi | Aliran WAL (asinkron pada praktikum ini) | Partisi + replication factor, metadata via consensus |
| Konflik tulis | Tidak ada (satu penulis) | Perlu penanganan konflik/konsistensi lebih rumit |
| Saat satu node mati | Promosi **manual** (`pg_promote()`), risiko kehilangan data dan split-brain | Node lain tetap melayani, tanpa promosi |
| Kompleksitas | Rendah, mudah dipahami | Lebih tinggi |
| Cocok untuk | Beban baca besar, tulis terpusat | Ketersediaan tulis tinggi |

---

## 8. Kesimpulan

1. **PostgreSQL:** streaming replication berhasil menyinkronkan primary ke replica lewat WAL. Replica terbukti read-only, otomatis mengikuti perubahan, dan dapat dipromosikan saat primary dimatikan. Namun promosinya manual, replikasinya asinkron, dan tidak ada pencegahan split-brain, sehingga sistem ini baru menyediakan *bahan* untuk High Availability, belum HA yang sesungguhnya.
2. **Apache Ignite:** ketiga node setara, semuanya dapat membaca dan menulis, dan perubahan di satu node terlihat di node lain tanpa promosi.
3. **Pilihan model** tidak ditentukan oleh mana yang lebih modern, melainkan oleh kebutuhan aplikasi: toleransi kehilangan data, kebutuhan penulisan, dan kesiapan tim merawat kompleksitasnya.

---

## 9. Catatan dan Pemecahan Masalah

| Gejala | Penyebab | Solusi |
|---|---|---|
| Error koneksi ke pipe Docker | Engine belum selesai boot | Tunggu status *Engine running* |
| `pg_basebackup ... Connection refused` di log replica | Primary belum siap | Normal; loop `until` akan mencoba ulang |
| Alias tidak dikenali | `env.sh` tidak di-`source` atau terminal baru | Jalankan `source env.sh` dari folder yang benar |
| Alias gagal menemukan container | Nama folder diubah | Sesuaikan nama container di `env.sh` |
| Perubahan `00_init.sql` tidak berefek | Init hanya jalan saat volume baru | Hapus data lama (`docker compose down`) lalu `up` lagi |
| Mount `sql` gagal di Git Bash | Konversi path Windows | Gunakan `MSYS_NO_PATHCONV=1` (sudah ada di `dclm`) |
| `cluster init` ditolak | Cluster sudah terbentuk | Cukup `cluster status`; init hanya sekali |
| Data hilang setelah `down` | Tidak ada named volume | Tambahkan volume jika data harus bertahan |

---

## 10. Referensi

1. PostgreSQL Global Development Group. (2025). *PostgreSQL 18 Documentation: High Availability, Load Balancing, and Replication.* <https://www.postgresql.org/docs/18/high-availability.html>
2. PostgreSQL Global Development Group. (2025). *PostgreSQL 18 Documentation: Write-Ahead Logging (WAL) dan pg_basebackup.* <https://www.postgresql.org/docs/18/wal.html>
3. Apache Software Foundation. (2025). *Apache Ignite 3 Documentation: Quick Start dan Explore SQL.* <https://ignite.apache.org/docs/ignite3/latest/quick-start/explore-sql>
4. Eremeykin. *How to Setup Single Primary PostgreSQL Replication with Docker Compose.* Medium. <https://medium.com/@eremeykin/how-to-setup-single-primary-postgresql-replication-with-docker-compose-98c48f233bbf>
5. Docker Inc. (2025). *Docker Documentation: Install Docker Engine dan Docker Compose.* <https://docs.docker.com/>
6. Özsu, M. T., & Valduriez, P. (2020). *Principles of Distributed Database Systems* (4th ed.). Springer.
7. Tanenbaum, A. S., & van Steen, M. (2023). *Distributed Systems* (4th ed.). Maarten van Steen.
8. Kleppmann, M. (2017). *Designing Data-Intensive Applications.* O'Reilly Media.
