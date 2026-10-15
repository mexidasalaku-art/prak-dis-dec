# Praktikum Minggu MODUL 03 - Sinkronisasi pada Sistem Terdistribusi

| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi |
| **Topik** | Sinkronisasi pada Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 |
| **Kelas** | IF-1 |

---


## Daftar Isi

- [3.1 Sinkronisasi Waktu](#31-sinkronisasi-waktu)
- [3.2 Vector Clock](#32-vector-clock)
- [3.3 Problem Tanpa Sinkronisasi](#33-problem-tanpa-sinkronisasi)
  - [3.3.1 Data Race / Race Conditions](#331-data-race--race-conditions)
  - [3.3.2 Deadlock](#332-deadlock)
- [3.4 Algoritma Raft](#34-algoritma-raft)

---

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
