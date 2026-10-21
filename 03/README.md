# Praktikum Minggu MODUL 03 - Sinkronisasi pada Sistem Terdistribusi

| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi |
| **Topik** | Sinkronisasi pada Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 |
| **Kelas** | IF-1 |

---


#  DASAR TEORI

<p align="justify">Pada sistem terdistribusi, setiap komputer memiliki jam sendiri yang bisa melenceng (clock drift), sehingga urutan log dan transaksi antar komputer dapat keliru; karena itu dipakai sinkronisasi waktu dengan NTP, yang bekerja lewat UDP port 123 dengan menukar empat cap waktu dengan server untuk menghitung selisih waktu (offset) dan lama perjalanan (delay), atau PTP yang lebih akurat karena dibantu perangkat keras, dengan Chrony dan NetTime sebagai klien yang dipakai pada praktikum ini. Karena tidak ada jam global yang benar-benar sinkron, urutan event ditentukan dari hubungan sebab-akibat menggunakan vector clock, yaitu penghitung untuk tiap proses yang bertambah pada setiap event dan digabung dengan mengambil nilai maksimum saat pesan diterima, sehingga dapat diketahui apakah suatu event terjadi lebih dulu atau konkuren dengan event lain. Selain itu, ketiadaan sinkronisasi pada program multithreaded menimbulkan data race, yaitu ketika beberapa thread mengakses data bersama dan hasilnya bergantung pada urutan eksekusi sehingga pembaruan bisa hilang (diatasi dengan lock agar hanya satu thread yang masuk ke bagian kritis), serta deadlock, yaitu ketika thread saling menunggu sumber daya yang dipegang satu sama lain sehingga tidak ada yang dapat melanjutkan (dicegah antara lain dengan mengunci sumber daya dalam urutan yang sama). Terakhir, agar beberapa node tetap sepakat meski sebagian gagal, digunakan algoritma konsensus Raft, di mana node berperan sebagai follower, candidate, atau leader; jika follower tidak menerima heartbeat dari leader sampai batas waktu, ia menjadi candidate dan meminta suara, dan candidate yang memperoleh suara mayoritas menjadi leader yang baru.</p>

---


#  TUJUAN PRAKTIKUM

1. Menjelaskan pentingnya sinkronisasi waktu pada sistem terdistribusi dan melakukan sinkronisasi waktu ke NTP server memakai Chrony atau NetTime.
2. Menjelaskan cara kerja vector clock dalam mengurutkan event pada sistem terdistribusi, serta mengimplementasikannya sebagai modul Python.
3. Mengamati dan menjelaskan terjadinya data race (race condition) dan deadlock pada program multithreaded.
4. Menerapkan mekanisme sinkronisasi untuk mencegah data race dan deadlock.
5. Menjelaskan algoritma Raft dalam pemilihan leader untuk mencapai konsensus, serta mensimulasikannya dengan Python.
---



#  PEMBAHASAN PRAKTIKUM

## PRAKTIK 1 - PROSES PADA SATU NODE

## 1 Sinkronisasi Waktu

Ada 2 protokol yang biasanya digunakan untuk sinkronisasi waktu: NTP (Network Time Protocol) dan PTP (Precision Time Protocol). Tapi disini saya menggunakan windows



### 1. Install NetTime (<https://www.timesynctool.com/>). Gunakan software tersebut untuk sinkronisasi waktu ke suatu NTP server.
-Next untuk lanjut

<img width="378" height="282" alt="01" src="https://github.com/user-attachments/assets/91ebfd0c-0a1c-49d5-94be-d8061de2d7d1" />

#### Pembahasan

-Lokasi instalasi

  <img width="379" height="279" alt="02" src="https://github.com/user-attachments/assets/a1f76449-ee72-4ffb-a63b-cf77ca67fb44" />

#### Pembahasan

-Nama folder

<img width="379" height="284" alt="03" src="https://github.com/user-attachments/assets/1d965713-37b5-499e-942d-4049bcbe8375" />

#### Pembahasan


-Install as Service

<img width="377" height="284" alt="04" src="https://github.com/user-attachments/assets/c9995cb5-4f0c-48a8-9a63-72d30ce415ac" />

#### Pembahasan

  
-Ringkasan instalasi

<img width="380" height="285" alt="05" src="https://github.com/user-attachments/assets/b0532d06-15d0-46ad-8051-287f2da439cb" />

#### Pembahasan
  
-Selesai Instal

<img width="376" height="281" alt="06" src="https://github.com/user-attachments/assets/96b51a1e-cde0-4ca0-9f97-d4236ce3c5ed" />


#### Pembahasan

### 2 Proses Sinkronisasi

<img width="385" height="277" alt="07_NetTime" src="https://github.com/user-attachments/assets/4b15cd6d-9301-4277-918e-c6bc716b8384" />

#### Pembahasan



---

## 2 Vector Clock

Vector clock digunakan untuk pengurutan event dalam suatu sistem terdistribusi. Berikut adalah contoh source code untuk vector clock (ada pada source code: `vclocks.py`). Source code diambil dari banyak sumber di Internet.

```python
# Code program vclocks.py
class VectorClock:
    def __init__(self, num_processes, process_id):
        self.clocks = [0] * num_processes
        self.process_id = process_id

    def increment(self):
        """Increments the local clock for the current process."""
        self.clocks[self.process_id] += 1

    def send_message(self):
        """Prepares the vector clock for sending with a message."""
        self.increment()
        return list(self.clocks)

    def receive_message(self, received_clocks):
        """Updates the vector clock upon receiving a message."""
        for i in range(len(self.clocks)):
            self.clocks[i] = max(
                self.clocks[i], received_clocks[i]
            )
        self.increment()

    def __str__(self):
        return f"P{self.process_id}: {self.clocks}"

    def happens_before(self, other_vector_clock):
        """
        Determines if this vector clock happens before another.
        A happens before B if all elements in A are less than
        or equal to corresponding elements in B, and at least
        one element in A is strictly less than B.
        """
        if self.clocks == other_vector_clock.clocks:
            return False

        all_le = True
        any_lt = False

        for i in range(len(self.clocks)):
            if self.clocks[i] > other_vector_clock.clocks[i]:
                return False

            if self.clocks[i] < other_vector_clock.clocks[i]:
                any_lt = True

        return all_le and any_lt

    def is_concurrent(self, other_vector_clock):
        """
        Determines if two vector clocks are concurrent.
        Two events are concurrent if neither happens before the other.
        """
        return not (
            self.happens_before(other_vector_clock)
            or other_vector_clock.happens_before(self)
        )


# Simulate a system with 3 processes
vc0 = VectorClock(num_processes=3, process_id=0)
vc1 = VectorClock(num_processes=3, process_id=1)
vc2 = VectorClock(num_processes=3, process_id=2)

print(vc0)
print(vc1)
print(vc2)

# Process 0 performs a local event
vc0.increment()
print(vc0)

# Process 0 sends a message to Process 1
message_from_p0 = vc0.send_message()
vc1.receive_message(message_from_p0)
print(vc0)
print(vc1)

# Process 2 performs a local event
vc2.increment()
print(vc2)

# Process 1 sends a message to Process 2
message_from_p1 = vc1.send_message()
vc2.receive_message(message_from_p1)
print(vc1) 
print(vc2)

# Check causality
print(f"VC0 happens before VC1: {vc0.happens_before(vc1)}")
print(f"VC1 happens before VC0: {vc1.happens_before(vc0)}")
print(f"VC0 is concurrent with VC2: {vc0.is_concurrent(vc2)}")

```
<img width="262" height="424" alt="09_Code_Program_clocks py" src="https://github.com/user-attachments/assets/5a957013-57a7-4fb5-82f5-6331629707bc" />

<img width="267" height="354" alt="10_Code_Program_clocks py" src="https://github.com/user-attachments/assets/a449ed02-4e10-4444-a748-f575a4f4d04f" />

#### Pembahasan

**Tugas:**

1. Jalankan program tersebut, amati keluarannya. Buat penjelasan dari keluaran tersebut: bandingkan dengan algoritma tersebut jika vector clocks dilaksanakan secara manual.

<img width="335" height="196" alt="01_Hasil_Output_clocks py" src="https://github.com/user-attachments/assets/ad8d6371-a694-4598-ad90-213e52e16655" />

#### Pembahasan

<p align="justify">Keluaran program sesuai dengan perhitungan manual algoritma vector clock. Ketiga proses (P0, P1, P2) dimulai dari [0,0,0]; setiap kejadian lokal atau pengiriman pesan menaikkan elemen milik proses itu sendiri (P0 menjadi [1,0,0] lalu [2,0,0]), sedangkan saat menerima pesan, proses mengambil nilai maksimum tiap elemen antara vektornya dan vektor pesan lalu menaikkan elemen miliknya, sehingga P1 menjadi [2,1,0] lalu [2,2,0] setelah mengirim, dan P2 menjadi max([0,0,1],[2,2,0]) = [2,2,1] kemudian [2,2,2]. Hasil pembandingannya juga benar: VC0 happens before VC1 bernilai True karena semua elemen VC0 lebih kecil atau sama dengan VC1, sebaliknya VC1 happens before VC0 bernilai False, dan VC0 is concurrent with VC2 bernilai False karena P2 sudah menerima informasi dari P0 melalui P1 ([2,0,0] ≤ [2,2,2]), sehingga keduanya berhubungan sebab-akibat, bukan konkuren.</p>

2. Buat modul Python untuk class `VectorClock` tersebut dan buatlah contoh cara menggunakan modul tersebut.
   - vektor_clock.py
     
     <img width="264" height="403" alt="12_vector_clock py" src="https://github.com/user-attachments/assets/0a9ef844-976c-4662-8287-79146427ccf5" />
     
     #### pembahasan

   - main.py
     
     <img width="286" height="375" alt="13_main py" src="https://github.com/user-attachments/assets/dc3804e1-0fc9-4715-b04d-87c862ebbf41" />

     #### Pembahasan

   - output main.py
     
       <img width="326" height="199" alt="14_output_main py" src="https://github.com/user-attachments/assets/a8a0fef3-6d65-4560-9589-16d18708b403" />

     #### Pembahasan

---

## 3 Problem Tanpa Sinkronisasi

Pada sistem terdistribusi, ketiadaan sinkronisasi bisa menghasilkan 2 masalah besar yaitu data race / race conditions dan deadlock. Pada program yang menggunakan model asynchronous maupun thread, pola pikir sekuensial tidak bisa digunakan karena penyelesaian satu task dengan task lainnya biasanya tidak bisa diprediksi. Berikut adalah contoh program multithreaded di Python (`multithreaded-example.py`).

<img width="230" height="241" alt="15_multithreads-example py" src="https://github.com/user-attachments/assets/03bcbe7d-1903-4d54-801d-caeada128aaf" />

#### Pembahasan

### Output

<img width="373" height="103" alt="16_output_multithreads-example py" src="https://github.com/user-attachments/assets/71d714f7-ccc6-43cd-b916-5a96a0af65bb" />

#### Pembahasan

### - Data Race / Race Conditions

Berikut adalah contoh data race / race conditions di Python (`race-conditions-01.py`).

<img width="259" height="168" alt="17_race-conditions-01 py" src="https://github.com/user-attachments/assets/ee37de55-2192-4514-a49e-dfc908850265" />

#### Pembahasan
 
**Tugas:**

### -Jalankan program tersebut.

<img width="360" height="35" alt="18_output_race-conditions-01 py" src="https://github.com/user-attachments/assets/16186982-ff82-4bcc-8511-18dcd1128c96" />

#### Pembahasan

### -Jelaskan menggunakan visualisasi (gambar dengan pensil/ballpoint kemudian difoto), mengapa terjadi data race / race conditions.

Berikut adalah contoh program untuk membuat supaya race conditions tersebut tidak terjadi (`race-conditions-02.py`):

<img width="276" height="188" alt="20_race-conditions-02 py" src="https://github.com/user-attachments/assets/00a0e955-6086-47e7-9d00-e7c9115b3424" />

#### Pembahasan


**Tugas:**

### -Jalankan program tersebut.

<img width="360" height="27" alt="21_output_race-conditions-02 py" src="https://github.com/user-attachments/assets/82092a14-8292-4e59-acc0-1eda38904598" />


#### Pembahasan

<p align="justify">Keluarannya hanya satu baris, yaitu “Mengambil sejumlah Rp 80. Saldo: Rp 20”, artinya hanya satu thread yang berhasil menarik uang dan saldo tetap wajar. Race condition tidak terjadi karena with counter_lock: memastikan hanya satu thread yang boleh menjalankan blok pengecekan dan pengurangan saldo pada satu waktu. Thread pertama yang masuk mengecek saldo (100 ≥ 80), lalu mengurangi saldo menjadi 20, sementara thread kedua menunggu lock dilepas. Saat thread kedua akhirnya masuk, saldo sudah 20 sehingga pengecekan 20 >= 80 gagal dan penarikan dilewati. Berbeda dengan versi tanpa lock, di mana kedua thread bisa lolos pengecekan bersamaan dan saldo menjadi negatif.</p>

### Deadlock

Berikut adalah contoh kondisi deadlock di Python (`deadlock-01.py`).

<img width="208" height="254" alt="22_deadlock-01 py" src="https://github.com/user-attachments/assets/84ac080c-565e-4a7e-bab8-c50889c722e0" />

#### Pembahasan

### -Jalankan program tersebut.

<img width="250" height="30" alt="23_output_deadlock-01 py" src="https://github.com/user-attachments/assets/69d3984d-3721-49c8-8111-972ed8b7e6cc" />

#### Pembahasan

### Jelaskan menggunakan visualisasi (gambar dengan pensil/ballpoint kemudian difoto), mengapa terjadi deadlock.

Berikut adalah contoh program untuk membuat supaya deadlock tersebut tidak terjadi (`deadlock-02.py`):

<img width="218" height="374" alt="25_deadlock-02 py" src="https://github.com/user-attachments/assets/308b84a1-26b7-43c9-a233-99d6e39b7a30" />

#### Pembahasan

**Tugas:**

### -Jalankan program tersebut.

<img width="341" height="89" alt="26_Output_deadlock-02 py" src="https://github.com/user-attachments/assets/a915f7f5-3942-4e82-87aa-c5b95a47b1af" />

#### Pembahasan

### -Amati keluarannya. Jelaskan mengapa deadlock tidak terjadi?
<p align="justify">Deadlock tidak terjadi karena setiap thread melepas lock pertamanya sebelum meminta lock kedua. Pada blok finally, Thread 1 menjalankan lock_a.release() dan Thread 2 menjalankan lock_b.release() sebelum keduanya memanggil acquire untuk lock berikutnya, sehingga tidak ada thread yang memegang satu lock sambil menunggu lock lain (tidak ada hold and wait maupun circular wait). Karena itu, Thread 2 bisa mendapat Lock A dan Thread 1 bisa mendapat Lock B, lalu program selesai dengan mencetak “Execution Finished”. Parameter timeout=5 juga berfungsi sebagai pengaman agar thread tidak menunggu selamanya, meskipun pada kasus ini tidak sempat terpakai.</p>
   

---

## 4 Algoritma Raft

Algoritma Raft banyak digunakan pada sistem terdistribusi, antara lain digunakan untuk mencapai konsensus. Berikut adalah simulasi algoritma Raft menggunakan Python yang diambil dari <https://www.c-sharpcorner.com/article/simulate-distributed-consensus-with-the-raft-protocol-simplified-using-python/>.

Class raft.py

<img width="329" height="445" alt="27_raft py" src="https://github.com/user-attachments/assets/1ab3a9b2-ecad-47b1-860c-ab90bfaa5cf8" />

<img width="397" height="399" alt="28_raft py" src="https://github.com/user-attachments/assets/41e1b752-1b40-4e78-8384-68ffe4d1b4c4" />


#### Pembahasan


### -Jalankan program tersebut.

<img width="305" height="439" alt="29_Output_raft py" src="https://github.com/user-attachments/assets/2a049d92-d6f2-47fa-81ec-4dfb5317710f" />

<img width="289" height="403" alt="30_Output_raft py" src="https://github.com/user-attachments/assets/7a7df193-93b5-4826-921d-777cb45da769" />

#### Pembahasan


### -Perhatikan keluaran program yang dijalankan tersebut. Dari keluaran program tersebut, jelaskan secara sederhana algoritma Raft untuk memilih koordinator (LEADER) menggunakan visualisasi (digambar dengan manual pensil/ballpoint dan kemudian difoto).

#### Pembahasan

### -Buatlah program tersebut menjadi modul Python dan kemudian buatlah contoh simulasinya menggunakan modul Python yang sudah Anda buat tersebut.

Class main2.py

<img width="267" height="449" alt="32_main2 py" src="https://github.com/user-attachments/assets/e505da5b-dec3-4332-94ae-84e49b73da65" />

#### Pembahasan

### -Output

<img width="311" height="415" alt="33_output_main py" src="https://github.com/user-attachments/assets/41abcf56-25c7-4814-bfe4-ad12b009a652" />

<img width="308" height="398" alt="34_output_main py" src="https://github.com/user-attachments/assets/7c5a101d-4138-40fe-a5e5-ba33e9ab5c1c" />

#### Pembahasan

  

# KESIMPULAN
