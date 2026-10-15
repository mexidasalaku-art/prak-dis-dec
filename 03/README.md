# Praktikum Minggu MODUL 03 - Sinkronisasi pada Sistem Terdistribusi

| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi |
| **Topik** | Sinkronisasi pada Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 |
| **Kelas** | IF-1 |

---

## 1. Tujuan Pembelajaran

Setelah menyelesaikan modul ini, peserta mampu:

1. Menjelaskan mengapa jam komputer perlu disinkronkan dan apa dampak jika tidak akurat.
2. Membedakan NTP dan SNTP serta menjelaskan konsep *stratum*, *offset*, dan *delay*.
3. Menghitung offset dan delay dari empat cap waktu (timestamp) pada pertukaran NTP.
4. Memeriksa dan mengatur sinkronisasi waktu di Windows menggunakan perintah `w32tm`.
5. Mendiagnosis kegagalan sinkronisasi yang umum, terutama yang terkait firewall dan port UDP 123.
6. Menyusun laporan hasil praktik secara runtut.

---

## 2. Prasyarat dan Alat

**Pengetahuan awal**

- Dasar penggunaan Command Prompt atau PowerShell.
- Pengertian dasar jaringan: alamat IP, port, protokol TCP/UDP.

**Alat dan bahan**

| Kebutuhan | Keterangan |
|---|---|
| Komputer dengan Windows 10/11 | Akun dengan hak Administrator |
| Koneksi internet | Port UDP 123 tidak diblokir |
| Command Prompt atau PowerShell | Dijalankan sebagai Administrator untuk Praktik 3 |
| (Opsional) Klien SNTP pihak ketiga | Dipakai pada Praktik 4 |

> **Peringatan:** Mengubah pengaturan waktu sistem memengaruhi seluruh aplikasi. Catat pengaturan awal sebelum mengubah apa pun agar bisa dikembalikan.

---

## 3. Materi Dasar

### 3.1 Mengapa waktu harus akurat?

Jam di komputer berasal dari osilator kristal yang tidak sempurna. Akibatnya jam bisa maju atau mundur beberapa detik per hari. Selisih waktu yang kecil pun dapat menimbulkan masalah:

- **Keamanan:** autentikasi seperti Kerberos dan sertifikat TLS bergantung pada waktu yang benar. Sertifikat bisa dianggap kedaluwarsa atau belum berlaku jika jam salah.
- **Log dan forensik:** menelusuri insiden lintas perangkat butuh cap waktu yang konsisten.
- **Basis data dan transaksi:** urutan kejadian dapat salah jika jam antarserver berbeda.
- **Penjadwalan:** tugas terjadwal berjalan di waktu yang keliru.

### 3.2 NTP dan SNTP

| | NTP (Network Time Protocol) | SNTP (Simple NTP) |
|---|---|---|
| Algoritma | Penyaringan dan seleksi dari banyak server | Sederhana, umumnya satu pembacaan |
| Akurasi | Sering di bawah 10 ms | Sekitar puluhan sampai ratusan ms |
| Penyesuaian jam | Mengatur *kecepatan* jam secara halus | Biasanya langsung *menetapkan* waktu |
| Cocok untuk | Server, infrastruktur | PC dan perangkat biasa |

Keduanya memakai format paket yang sama dan berjalan di atas **UDP port 123**.

### 3.3 Istilah penting

- **UTC (Coordinated Universal Time):** acuan waktu dunia. NTP bekerja dengan UTC; zona waktu dan daylight saving diurus oleh sistem operasi.
- **Stratum:** tingkat kedekatan dengan sumber waktu referensi.
  - Stratum 0: jam referensi (jam atom, GPS), tidak terhubung langsung ke jaringan.
  - Stratum 1: server yang terhubung langsung ke stratum 0.
  - Stratum 2: server yang sinkron ke stratum 1, dan seterusnya. Semakin besar angkanya, semakin jauh dari sumber.
- **Offset:** selisih antara jam lokal dan jam server.
- **Delay (round-trip delay):** lama perjalanan permintaan ke server dan kembali.
- **NTP Pool:** kumpulan server NTP sukarela yang dipakai bersama, misalnya `pool.ntp.org` dan varian regional seperti `id.pool.ntp.org`.

### 3.4 Cara menghitung offset dan delay

Satu pertukaran NTP menghasilkan empat cap waktu:

| Simbol | Arti | Diukur oleh |
|---|---|---|
| T1 | Waktu klien mengirim permintaan | Jam klien |
| T2 | Waktu server menerima permintaan | Jam server |
| T3 | Waktu server mengirim balasan | Jam server |
| T4 | Waktu klien menerima balasan | Jam klien |

```
offset = ((T2 - T1) + (T3 - T4)) / 2
delay  = (T4 - T1) - (T3 - T2)
```

**Contoh hitungan.** Misalkan T1 = 10.000, T2 = 10.150, T3 = 10.152, T4 = 10.040 (dalam milidetik pada skala masing-masing jam).

```
offset = ((10.150 - 10.000) + (10.152 - 10.040)) / 2
       = (150 + 112) / 2
       = 131 ms

delay  = (10.040 - 10.000) - (10.152 - 10.150)
       = 40 - 2
       = 38 ms
```

Artinya jam klien tertinggal sekitar 131 ms dari jam server, dengan waktu tempuh pulang-pergi 38 ms.

> **Asumsi penting:** rumus ini mengandaikan waktu tempuh pergi dan pulang sama besar. Jika jaringan tidak simetris, offset yang dihitung ikut menyimpang. Inilah batas akurasi SNTP di jaringan publik.

### 3.5 Mengapa satu server saja berisiko?

Klien yang hanya bertanya ke satu server tidak punya pembanding. Jika server itu keliru (sengaja atau tidak), jam klien ikut salah. Karena itu klien yang baik membandingkan beberapa server, terutama ketika selisih waktunya besar.

---

## 4. Praktik 1: Mengamati Kondisi Waktu Sistem

**Tujuan:** mengetahui keadaan awal sebelum perubahan apa pun.

Buka Command Prompt (Administrator), lalu jalankan:

```
w32tm /query /status
```

Catat nilai berikut pada lembar hasil:

| Kolom | Arti | Hasil Anda |
|---|---|---|
| Source | Sumber waktu yang dipakai | |
| Stratum | Tingkat stratum sumber | |
| Last Successful Sync Time | Waktu sinkronisasi terakhir yang berhasil | |
| Poll Interval | Selang antar permintaan | |

Lalu periksa konfigurasi server:

```
w32tm /query /peers
w32tm /query /configuration
```

**Pertanyaan pemantik**

1. Dari mana komputer Anda mengambil waktu saat ini?
2. Kapan terakhir kali sinkronisasi berhasil?
3. Jika layanan waktu tidak berjalan, apa yang tampil?

> Jika muncul pesan bahwa layanan belum berjalan, mulai dengan `net start w32time`.

---

## 5. Praktik 2: Mengukur Selisih Waktu ke Server NTP

**Tujuan:** melihat offset sebenarnya antara komputer Anda dan server NTP, tanpa mengubah jam.

Perintah `stripchart` hanya membaca dan menampilkan selisih:

```
w32tm /stripchart /computer:id.pool.ntp.org /samples:5 /dataonly
```

Contoh bentuk keluaran:

```
Tracking id.pool.ntp.org [xxx.xxx.xxx.xxx:123].
The current time is ...
12:00:00, +00.0123456s
12:00:02, +00.0119876s
...
```

Angka seperti `+00.0123456s` adalah offset dalam detik (positif berarti jam lokal tertinggal dari server).

Ulangi dengan dua server lain, misalnya `time.windows.com` dan `time.google.com`.

**Tabel hasil**

| Server | Rata-rata offset (detik) | Catatan |
|---|---|---|
| id.pool.ntp.org | | |
| time.windows.com | | |
| time.google.com | | |

**Pertanyaan pemantik**

1. Apakah ketiga server memberi offset yang mirip? Jika berbeda, apa kemungkinan penyebabnya?
2. Berapa selisih terbesar yang Anda dapatkan, dan apakah masih wajar?

---

## 6. Praktik 3: Mengatur Sinkronisasi di Windows

**Tujuan:** mengganti server waktu dan memaksa sinkronisasi.

> Lakukan di komputer pribadi atau lab yang diizinkan. Pada perangkat milik kantor atau kampus yang dikelola kebijakan (Group Policy), pengaturan ini bisa tertimpa atau dilarang.

**Langkah 1. Catat konfigurasi lama**

```
w32tm /query /configuration > konfigurasi-awal.txt
```

**Langkah 2. Atur server baru**

```
w32tm /config /manualpeerlist:"id.pool.ntp.org" /syncfromflags:manual /update
```

**Langkah 3. Paksa sinkronisasi**

```
w32tm /resync
```

**Langkah 4. Verifikasi**

```
w32tm /query /status
w32tm /query /peers
```

Pastikan kolom *Source* kini menunjuk ke server yang Anda atur dan *Last Successful Sync Time* terbaru.

**Langkah 5. Pengaturan lewat antarmuka (alternatif)**

Settings, Time & language, Date & time, lalu bagian *Additional settings* dan klik *Sync now*. Server dapat diganti melalui Control Panel (Date and Time, tab *Internet Time*).

**Pertanyaan pemantik**

1. Apa beda tampilan `Source` sebelum dan sesudah pengaturan?
2. Mengapa memakai pool regional (`id.pool.ntp.org`) lebih disarankan daripada satu server tunggal?

---

## 7. Praktik 4: Mencoba Klien SNTP Pihak Ketiga

**Tujuan:** membandingkan klien bawaan Windows dengan klien SNTP lain. Bagian ini **opsional**.

NetTime adalah salah satu contoh klien SNTP gratis untuk Windows. Unduh hanya dari situs resmi pengembangnya, jalankan installer, lalu amati:

- Berapa **offset** dan **lag** yang ditampilkan untuk tiap server?
- Berapa lama **selang sinkronisasi** bawaannya?
- Apa yang terjadi jika semua server gagal dihubungi?

**Tabel perbandingan**

| Aspek | Klien bawaan Windows | Klien pihak ketiga |
|---|---|---|
| Antarmuka | | |
| Jumlah server yang bisa dipakai | | |
| Informasi offset/lag | | |
| Kemudahan konfigurasi | | |

> **Catatan keamanan:** file installer berjalan dengan hak tinggi dan memasang layanan di sistem. Unduh dari sumber resmi, periksa tanda tangan digital, dan lebih baik uji di mesin virtual terlebih dahulu.

---

## 8. Pemecahan Masalah

| Gejala | Kemungkinan penyebab | Tindakan |
|---|---|---|
| Sinkronisasi gagal ("semua server gagal") | Firewall memblokir UDP 123 | Periksa firewall perangkat dan jaringan; coba dari jaringan lain (misalnya hotspot ponsel) |
| `w32tm /resync` menolak berjalan | Layanan Windows Time belum aktif | `net start w32time`, lalu ulangi |
| Pesan akses ditolak | Terminal tidak berjalan sebagai Administrator | Buka ulang sebagai Administrator |
| Waktu selisih tepat satu jam | Zona waktu atau daylight saving salah | Periksa zona waktu di pengaturan Windows; NTP sendiri memakai UTC |
| Offset besar dan tidak konsisten antar server | Server tidak sehat atau jaringan tidak simetris | Pakai beberapa server dan bandingkan |
| Hasil kembali ke nilai lama setelah di-restart | Kebijakan organisasi menimpa pengaturan | Hubungi administrator jaringan |
| Waktu salah lagi setelah mati total | Baterai CMOS lemah atau habis | Ganti baterai CMOS |

**Alur diagnosis singkat**

1. Pastikan layanan waktu berjalan.
2. Pastikan DNS dapat me-resolve nama server (`nslookup id.pool.ntp.org`).
3. Pastikan UDP 123 tidak diblokir.
4. Coba server lain.
5. Periksa zona waktu dan kebijakan perangkat.

---

## 9. Latihan Mandiri

**Soal 1 (hitungan).** Diketahui T1 = 5.000, T2 = 5.080, T3 = 5.081, T4 = 5.030 (ms). Hitung offset dan delay.

**Soal 2 (konsep).** Mengapa NTP memakai UTC dan tidak langsung memakai waktu lokal?

**Soal 3 (analisis).** Sebuah klien SNTP hanya memakai satu server. Server tersebut tiba-tiba memberi waktu yang selisih 2 jam. Jelaskan risikonya dan bagaimana klien yang membandingkan beberapa server dapat menghindarinya.

**Soal 4 (keamanan).** Sebutkan dua dampak keamanan jika jam sebuah server tertinggal beberapa jam.

**Soal 5 (skenario).** Sinkronisasi gagal hanya ketika terhubung ke Wi-Fi kampus, tetapi berhasil lewat hotspot ponsel. Apa dugaan Anda dan bagaimana membuktikannya?

<details>
<summary>Kunci jawaban Soal 1 dan 2</summary>

**Soal 1**

```
offset = ((5.080 - 5.000) + (5.081 - 5.030)) / 2 = (80 + 51) / 2 = 65,5 ms
delay  = (5.030 - 5.000) - (5.081 - 5.080)       = 30 - 1       = 29 ms
```

**Soal 2.** UTC adalah acuan tunggal yang tidak berubah oleh zona waktu atau daylight saving. Dengan satu acuan, semua perangkat di mana pun bisa bertukar waktu tanpa ambigu, dan konversi ke waktu lokal diserahkan ke sistem operasi.

</details>

---

## 10. Tugas dan Penilaian

### Tugas laporan

Susun laporan singkat (maksimal 4 halaman) berisi:

1. Hasil Praktik 1 sampai 3 (tabel, tangkapan layar, perintah yang dipakai).
2. Jawaban pertanyaan pemantik.
3. Jawaban Latihan Mandiri beserta cara hitungnya.
4. Satu masalah yang Anda temui dan cara menyelesaikannya.
5. Kesimpulan.

### Rubrik penilaian

| Komponen | Bobot | Kriteria |
|---|---|---|
| Kelengkapan praktik | 30% | Semua tabel dan tangkapan layar terisi dan sesuai langkah |
| Ketepatan analisis | 25% | Jawaban pertanyaan pemantik benar dan beralasan |
| Latihan mandiri | 25% | Hitungan dan penjelasan benar |
| Pemecahan masalah | 10% | Diagnosis runtut dan masuk akal |
| Kerapian laporan | 10% | Sistematis, bahasa jelas, sumber dicantumkan |

---

## 11. Rangkuman

- Jam komputer cenderung melenceng, dan akurasi waktu penting bagi keamanan, log, dan transaksi.
- NTP dan SNTP berjalan di UDP port 123 dan bekerja dengan UTC.
- Offset dan delay dihitung dari empat cap waktu (T1 sampai T4); akurasinya bergantung pada kesimetrisan jaringan.
- Memakai beberapa server melindungi dari satu sumber waktu yang keliru.
- Penyebab kegagalan sinkronisasi yang paling umum adalah firewall yang memblokir UDP 123.

---

## 12. Referensi

- RFC 5905, *Network Time Protocol Version 4: Protocol and Algorithms Specification*.
- RFC 4330, *Simple Network Time Protocol (SNTP) Version 4*.
- Dokumentasi Microsoft untuk perintah `w32tm`.
- NTP Pool Project: <https://www.pool.ntp.org>
- Halaman proyek NetTime (untuk Praktik 4 opsional).
