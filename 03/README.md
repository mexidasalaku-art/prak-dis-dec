# Praktikum Minggu MODUL 03 - Sinkronisasi pada Sistem Terdistribusi

| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi |
| **Topik** | Sinkronisasi pada Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 |
| **Kelas** | IF-1 |

---


#  Dasar Teori

Pada sistem terdistribusi, setiap komputer memiliki jam sendiri yang bisa melenceng (clock drift), sehingga urutan log dan transaksi antar komputer dapat keliru; karena itu dipakai sinkronisasi waktu dengan NTP, yang bekerja lewat UDP port 123 dengan menukar empat cap waktu dengan server untuk menghitung selisih waktu (offset) dan lama perjalanan (delay), atau PTP yang lebih akurat karena dibantu perangkat keras, dengan Chrony dan NetTime sebagai klien yang dipakai pada praktikum ini. Karena tidak ada jam global yang benar-benar sinkron, urutan event ditentukan dari hubungan sebab-akibat menggunakan vector clock, yaitu penghitung untuk tiap proses yang bertambah pada setiap event dan digabung dengan mengambil nilai maksimum saat pesan diterima, sehingga dapat diketahui apakah suatu event terjadi lebih dulu atau konkuren dengan event lain. Selain itu, ketiadaan sinkronisasi pada program multithreaded menimbulkan data race, yaitu ketika beberapa thread mengakses data bersama dan hasilnya bergantung pada urutan eksekusi sehingga pembaruan bisa hilang (diatasi dengan lock agar hanya satu thread yang masuk ke bagian kritis), serta deadlock, yaitu ketika thread saling menunggu sumber daya yang dipegang satu sama lain sehingga tidak ada yang dapat melanjutkan (dicegah antara lain dengan mengunci sumber daya dalam urutan yang sama). Terakhir, agar beberapa node tetap sepakat meski sebagian gagal, digunakan algoritma konsensus Raft, di mana node berperan sebagai follower, candidate, atau leader; jika follower tidak menerima heartbeat dari leader sampai batas waktu, ia menjadi candidate dan meminta suara, dan candidate yang memperoleh suara mayoritas menjadi leader yang baru. 

---


#  Tujuan Praktikum

1. Menjelaskan pentingnya sinkronisasi waktu pada sistem terdistribusi dan melakukan sinkronisasi waktu ke NTP server memakai Chrony atau NetTime.
2. Menjelaskan cara kerja vector clock dalam mengurutkan event pada sistem terdistribusi, serta mengimplementasikannya sebagai modul Python.
3. Mengamati dan menjelaskan terjadinya data race (race condition) dan deadlock pada program multithreaded.
4. Menerapkan mekanisme sinkronisasi untuk mencegah data race dan deadlock.
5. Menjelaskan algoritma Raft dalam pemilihan leader untuk mencapai konsensus, serta mensimulasikannya dengan Python.
---



#  PEMBAHASAN PRAKTIKUM

## PRAKTIK 1 - PROSES PADA SATU NODE

## 3.1 Sinkronisasi Waktu

Ada 2 protokol yang biasanya digunakan untuk sinkronisasi waktu: NTP (Network Time Protocol) dan PTP (Precision Time Protocol). Tapi disini saya menggunakan windows


**Windows**

1. Install NetTime (<https://www.timesynctool.com/>). Gunakan software tersebut untuk sinkronisasi waktu ke suatu NTP server.
2. Jelaskan proses sinkronisasi tersebut.

---

## 3.2 Vector Clock

Vector clock digunakan untuk pengurutan event dalam suatu sistem terdistribusi. Berikut adalah contoh source code untuk vector clock (ada pada source code: `vclocks.py`). Source code diambil dari banyak sumber di Internet.

```python
# Tempel isi vclocks.py di sini
```

**Tugas:**

1. Jalankan program tersebut, amati keluarannya. Buat penjelasan dari keluaran tersebut: bandingkan dengan algoritma tersebut jika vector clocks dilaksanakan secara manual.
2. Buat modul Python untuk class `VectorClock` tersebut dan buatlah contoh cara menggunakan modul tersebut.

---

## 3.3 Problem Tanpa Sinkronisasi

Pada sistem terdistribusi, ketiadaan sinkronisasi bisa menghasilkan 2 masalah besar yaitu data race / race conditions dan deadlock. Pada program yang menggunakan model asynchronous maupun thread, pola pikir sekuensial tidak bisa digunakan karena penyelesaian satu task dengan task lainnya biasanya tidak bisa diprediksi. Berikut adalah contoh program multithreaded di Python (`multithreaded-example.py`).

```python
# Tempel isi multithreaded-example.py di sini
```

**Tugas:**

1. Jalankan program tersebut sampai Anda mendapatkan keluaran yang berbeda.
2. Capture keluaran program tersebut dan jelaskan mengapa bisa berbeda.

### 3.3.1 Data Race / Race Conditions

Berikut adalah contoh data race / race conditions di Python (`race-conditions-01.py`).

```python
# Tempel isi race-conditions-01.py di sini
```

**Tugas:**

1. Jalankan program tersebut.
2. Jelaskan menggunakan visualisasi (gambar dengan pensil/ballpoint kemudian difoto), mengapa terjadi data race / race conditions.

Berikut adalah contoh program untuk membuat supaya race conditions tersebut tidak terjadi (`race-conditions-02.py`):

```python
# Tempel isi race-conditions-02.py di sini
```

**Tugas:**

1. Jalankan program tersebut.
2. Amati keluarannya. Jelaskan mengapa race-conditions tidak terjadi?

### 3.3.2 Deadlock

Berikut adalah contoh kondisi deadlock di Python (`deadlock-01.py`).

```python
# Tempel isi deadlock-01.py di sini
```

**Tugas:**

1. Jalankan program tersebut.
2. Jelaskan menggunakan visualisasi (gambar dengan pensil/ballpoint kemudian difoto), mengapa terjadi deadlock.

Berikut adalah contoh program untuk membuat supaya deadlock tersebut tidak terjadi (`deadlock-02.py`):

```python
# Tempel isi deadlock-02.py di sini
```

**Tugas:**

1. Jalankan program tersebut.
2. Amati keluarannya. Jelaskan mengapa deadlock tidak terjadi?

---

## 3.4 Algoritma Raft

Algoritma Raft banyak digunakan pada sistem terdistribusi, antara lain digunakan untuk mencapai konsensus. Berikut adalah simulasi algoritma Raft menggunakan Python yang diambil dari <https://www.c-sharpcorner.com/article/simulate-distributed-consensus-with-the-raft-protocol-simplified-using-python/>.

File: `raft.py`

```python
# Tempel isi raft.py di sini
```

**Tugas:**

1. Jalankan program tersebut.
2. Perhatikan keluaran program yang dijalankan tersebut. Dari keluaran program tersebut, jelaskan secara sederhana algoritma Raft untuk memilih koordinator (LEADER) menggunakan visualisasi (digambar dengan manual pensil/ballpoint dan kemudian difoto).
3. Buatlah program tersebut menjadi modul Python dan kemudian buatlah contoh simulasinya menggunakan modul Python yang sudah Anda buat tersebut.
