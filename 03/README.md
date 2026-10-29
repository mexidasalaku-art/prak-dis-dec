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
<p align="justify">Gambar ini menampilkan halaman awal Setup Wizard untuk menginstal NetTime, aplikasi yang menyinkronkan jam komputer dengan server waktu internet. Wizard menyarankan agar semua aplikasi lain ditutup sebelum melanjutkan. Tombol Next > dipakai untuk lanjut ke tahap berikutnya, sedangkan Cancel untuk membatalkan instalasi.</p>

-Lokasi instalasi

  <img width="379" height="279" alt="02" src="https://github.com/user-attachments/assets/a1f76449-ee72-4ffb-a63b-cf77ca67fb44" />

#### Pembahasan
<p align="justify">Gambar ini menampilkan tahap pemilihan lokasi instalasi NetTime. Lokasi bawaannya adalah C:\Program Files (x86)\NetTime dan dapat diganti lewat tombol Browse.... Instalasi membutuhkan ruang disk minimal 1,9 MB. Klik Next > untuk melanjutkan.</p>

-Nama folder

<img width="379" height="284" alt="03" src="https://github.com/user-attachments/assets/1d965713-37b5-499e-942d-4049bcbe8375" />

#### Pembahasan
<p align="justify">Halaman ringkasan sebelum instalasi dimulai: lokasi tujuan C:\Program Files (x86)\NetTime, folder Start Menu NetTime, dan tugas tambahan Install as Service. Klik Install untuk memulai, atau < Back untuk mengubah pengaturan.</p>


-Install as Service

<img width="377" height="284" alt="04" src="https://github.com/user-attachments/assets/c9995cb5-4f0c-48a8-9a63-72d30ce415ac" />

#### Pembahasan
<p align="justify">Tahap tugas tambahan. Opsi “Install as Service (Recommended)” dicentang agar NetTime berjalan sebagai layanan di latar belakang dan menyinkronkan waktu otomatis tanpa harus dibuka manual.</p>

  
-Ringkasan instalasi

<img width="380" height="285" alt="05" src="https://github.com/user-attachments/assets/b0532d06-15d0-46ad-8051-287f2da439cb" />

#### Pembahasan
<p align="justify">Tahap pemilihan folder Start Menu untuk shortcut program. Nama bawaannya NetTime dan bisa diganti lewat Browse.</p>
  
-Selesai Instal

<img width="376" height="281" alt="06" src="https://github.com/user-attachments/assets/96b51a1e-cde0-4ca0-9f97-d4236ce3c5ed" />


#### Pembahasan
<p align="justify">Ini tahap terakhir: instalasi NetTime sudah selesai. Opsi “Start NetTime now” dicentang agar aplikasi langsung berjalan, dan tombol Finish menutup wizard.</p>

### 2 Proses Sinkronisasi

<img width="385" height="277" alt="07_NetTime" src="https://github.com/user-attachments/assets/4b15cd6d-9301-4277-918e-c6bc716b8384" />

#### Pembahasan
<p align="justify">Gambar ini menampilkan jendela utama NetTime yang sudah berjalan sebagai Windows Service. Status “Time is synchronized” berarti jam komputer sudah sinkron dengan server waktu, dengan sinkronisasi terakhir pukul 19:30:29 (selisih -39 ms) dan percobaan berikutnya 11 jam 56 menit lagi. Dari daftar server, hanya 0.nettime.pool.ntp.org yang aktif (status Good, lag 46 ms), sedangkan tiga lainnya Not Used sebagai cadangan. Kolom Last Error kosong, artinya tidak ada kesalahan.</p>



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

<p align="justify">File ini berisi kelas VectorClock beserta simulasi di dalamnya. Kelas ini memiliki atribut clocks (counter tiap proses) dan process_id, dengan metode increment() untuk menambah counter sendiri, send_message() untuk menambah counter lalu mengirim salinan vector clock, dan receive_message() untuk mengambil nilai maksimum tiap elemen lalu menambah counter sendiri. Metode happens_before() memeriksa hubungan sebab-akibat (semua elemen A ≤ B dan minimal satu elemen A < B), sedangkan is_concurrent() menyatakan dua kejadian konkuren jika tidak ada yang happens-before yang lain. Pada bagian simulasi, tiga proses dibuat lalu dijalankan: P0 melakukan event lokal, P0 mengirim pesan ke P1, P2 melakukan event lokal, P1 mengirim pesan ke P2, dan terakhir dicek hubungan kausalitasnya. </p>

**Tugas:**

1. Jalankan program tersebut, amati keluarannya. Buat penjelasan dari keluaran tersebut: bandingkan dengan algoritma tersebut jika vector clocks dilaksanakan secara manual.

<img width="335" height="196" alt="01_Hasil_Output_clocks py" src="https://github.com/user-attachments/assets/ad8d6371-a694-4598-ad90-213e52e16655" />

#### Pembahasan

<p align="justify">Keluaran program sesuai dengan perhitungan manual algoritma vector clock. Ketiga proses (P0, P1, P2) dimulai dari [0,0,0]; setiap kejadian lokal atau pengiriman pesan menaikkan elemen milik proses itu sendiri (P0 menjadi [1,0,0] lalu [2,0,0]), sedangkan saat menerima pesan, proses mengambil nilai maksimum tiap elemen antara vektornya dan vektor pesan lalu menaikkan elemen miliknya, sehingga P1 menjadi [2,1,0] lalu [2,2,0] setelah mengirim, dan P2 menjadi max([0,0,1],[2,2,0]) = [2,2,1] kemudian [2,2,2]. Hasil pembandingannya juga benar: VC0 happens before VC1 bernilai True karena semua elemen VC0 lebih kecil atau sama dengan VC1, sebaliknya VC1 happens before VC0 bernilai False, dan VC0 is concurrent with VC2 bernilai False karena P2 sudah menerima informasi dari P0 melalui P1 ([2,0,0] ≤ [2,2,2]), sehingga keduanya berhubungan sebab-akibat, bukan konkuren.</p>

2. Buat modul Python untuk class `VectorClock` tersebut dan buatlah contoh cara menggunakan modul tersebut.
   - vektor_clock.py
     
     <img width="264" height="403" alt="12_vector_clock py" src="https://github.com/user-attachments/assets/0a9ef844-976c-4662-8287-79146427ccf5" />
     
     #### pembahasan
<p align="justify">Ini versi modular dari kelas VectorClock dengan komentar berbahasa Indonesia. Logikanya sama, tetapi happens_before() lebih ringkas karena hanya memakai any_lt (variabel all_le di versi sebelumnya tidak berpengaruh). Kelas ini dipisah ke file sendiri agar bisa diimpor.</p>

   - main.py
     
     <img width="286" height="375" alt="13_main py" src="https://github.com/user-attachments/assets/dc3804e1-0fc9-4715-b04d-87c862ebbf41" />

     #### Pembahasan

     <p align="justify">Program utama yang mengimpor VectorClock dari vector_clock dan menjalankan simulasi yang sama dengan Gambar 2. Bedanya, tiap tahap diberi judul seperti “=== Proses 0 mengirim pesan ke Proses 1 ===” agar output lebih mudah dibaca.</p>

   - output main.py
     
       <img width="326" height="199" alt="14_output_main py" src="https://github.com/user-attachments/assets/a8a0fef3-6d65-4560-9589-16d18708b403" />

     #### Pembahasan

<p align="justify">Output program vector clock dari main.py. Semua clock mulai dari [0, 0, 0]. P0 melakukan event lokal menjadi [1, 0, 0], lalu mengirim pesan menjadi [2, 0, 0], sedangkan P1 menjadi [2, 1, 0] setelah menerima. P2 menjadi [0, 0, 1] setelah event lokal, lalu [2, 2, 2] setelah menerima pesan dari P1 (P1 juga naik menjadi [2, 2, 0] saat mengirim). Hasil kausalitas: VC0 happens before VC1 = True, VC1 happens before VC0 = False, dan VC0 concurrent dengan VC2 = False karena VC0 [2,0,0] terjadi sebelum VC2 [2,2,2].</p>

---

## 3 Problem Tanpa Sinkronisasi

<p align="justify">Pada sistem terdistribusi, ketiadaan sinkronisasi bisa menghasilkan 2 masalah besar yaitu data race / race conditions dan deadlock. Pada program yang menggunakan model asynchronous maupun thread, pola pikir sekuensial tidak bisa digunakan karena penyelesaian satu task dengan task lainnya biasanya tidak bisa diprediksi. Berikut adalah contoh program multithreaded di Python (`multithreaded-example.py`).</p>

<img width="230" height="241" alt="15_multithreads-example py" src="https://github.com/user-attachments/assets/03bcbe7d-1903-4d54-801d-caeada128aaf" />

#### Pembahasan

<p align="justify">Program ini membuat lima thread (A sampai E) menggunakan modul threading, yang masing-masing menjalankan fungsi task() dengan time.sleep(5) untuk mensimulasikan operasi I/O-bound. Semua thread dijalankan dengan start(), lalu join() memastikan program utama menunggu semuanya selesai sebelum mencetak “All tasks completed.”</p>

### Output

<img width="373" height="103" alt="16_output_multithreads-example py" src="https://github.com/user-attachments/assets/71d714f7-ccc6-43cd-b916-5a96a0af65bb" />

#### Pembahasan

<p align="justify">Kelima task langsung mulai hampir bersamaan, lalu selesai setelah 5 detik. Karena berjalan paralel (konkuren), total waktunya sekitar 5 detik, bukan 25 detik jika dijalankan berurutan. Urutan selesai tidak selalu sama dengan urutan mulai (di sini A, B, E, C, D), karena penjadwalan thread ditentukan oleh sistem operasi.</p>

### - Data Race / Race Conditions

Berikut adalah contoh data race / race conditions di Python (`race-conditions-01.py`).

<img width="259" height="168" alt="17_race-conditions-01 py" src="https://github.com/user-attachments/assets/ee37de55-2192-4514-a49e-dfc908850265" />

#### Pembahasan

<p align="justify">Program ini memiliki variabel global balance = 100 dan fungsi withdraw(amount) yang mengecek balance >= amount, tidur 0,01 detik, lalu mengurangi saldo. Dua thread (t1 dan t2) sama-sama menarik Rp80 tanpa pengaman (lock), sehingga pengecekan dan pengurangan saldo tidak berjalan sebagai satu kesatuan.</p>
 
**Tugas:**

### -Jalankan program tersebut.

<img width="360" height="35" alt="18_output_race-conditions-01 py" src="https://github.com/user-attachments/assets/16186982-ff82-4bcc-8511-18dcd1128c96" />

#### Pembahasan

<p align="justify">Output menunjukkan saldo akhir Rp20, lalu Rp-60. Ini bukti race condition: kedua thread lolos pengecekan karena saldo masih 100 saat dicek, padahal seharusnya penarikan kedua ditolak.</p>

### -Jelaskan menggunakan visualisasi (gambar dengan pensil/ballpoint kemudian difoto), mengapa terjadi data race / race conditions.

<img width="1200" height="1600" alt="19_Visualisasi gambar" src="https://github.com/user-attachments/assets/0771b7a2-0f45-4afe-b0f7-2750a8a1bd55" />

#### Pembahasan

<p align="justify">Diagram menggambarkan salah satu kemungkinan alur eksekusi. Thread 1 dan Thread 2 sama-sama membaca saldo 100 dan mengecek 100 >= 80 (TRUE), lalu menunggu. Thread 1 mengurangi saldo menjadi 20 dan menampilkan Rp20, kemudian Thread 2 tetap mengurangi dari nilai yang sudah berubah sehingga saldo menjadi -60.</p>


Berikut adalah contoh program untuk membuat supaya race conditions tersebut tidak terjadi (`race-conditions-02.py`):

<img width="276" height="188" alt="20_race-conditions-02 py" src="https://github.com/user-attachments/assets/00a0e955-6086-47e7-9d00-e7c9115b3424" />

#### Pembahasan

<p align="justify">Ini versi perbaikan dengan threading.Lock() bernama counter_lock. Blok with counter_lock: membungkus pengecekan, sleep, dan pengurangan saldo, sehingga hanya satu thread yang boleh masuk pada satu waktu.</p>


**Tugas:**

### -Jalankan program tersebut.

<img width="360" height="27" alt="21_output_race-conditions-02 py" src="https://github.com/user-attachments/assets/82092a14-8292-4e59-acc0-1eda38904598" />

#### Pembahasan

<p align="justify">Keluarannya hanya satu baris, yaitu “Mengambil sejumlah Rp 80. Saldo: Rp 20”, artinya hanya satu thread yang berhasil menarik uang dan saldo tetap wajar. Race condition tidak terjadi karena with counter_lock: memastikan hanya satu thread yang boleh menjalankan blok pengecekan dan pengurangan saldo pada satu waktu. Thread pertama yang masuk mengecek saldo (100 ≥ 80), lalu mengurangi saldo menjadi 20, sementara thread kedua menunggu lock dilepas. Saat thread kedua akhirnya masuk, saldo sudah 20 sehingga pengecekan 20 >= 80 gagal dan penarikan dilewati. Berbeda dengan versi tanpa lock, di mana kedua thread bisa lolos pengecekan bersamaan dan saldo menjadi negatif.</p>

### Deadlock

Berikut adalah contoh kondisi deadlock di Python (`deadlock-01.py`).

<img width="208" height="254" alt="22_deadlock-01 py" src="https://github.com/user-attachments/assets/84ac080c-565e-4a7e-bab8-c50889c722e0" />

#### Pembahasan

<p align="justify">Program ini membuat dua lock, lock_a dan lock_b. Thread 1 mengunci A lalu mencoba mengunci B, sedangkan Thread 2 mengunci B lalu mencoba mengunci A, dengan sleep(1) di antaranya untuk memperbesar peluang deadlock. Karena urutan pengambilan lock berlawanan, kedua thread akan saling menunggu lock yang dipegang lawannya dan program berhenti (hang) tanpa pernah selesai. Solusinya, semua thread harus mengambil lock dalam urutan yang sama (misalnya A lalu B).</p>

### -Jalankan program tersebut.

<img width="250" height="30" alt="23_output_deadlock-01 py" src="https://github.com/user-attachments/assets/69d3984d-3721-49c8-8111-972ed8b7e6cc" />

#### Pembahasan

<p align="justify">Output hanya menampilkan dua baris: “Thread 1: Locked A, waiting for B...” dan “Thread 2: Locked B, waiting for A...”. Setelah itu program berhenti (hang) dan tidak pernah mencetak “Locked both”. Ini bukti deadlock: Thread 1 memegang A dan menunggu B, sedangkan Thread 2 memegang B dan menunggu A.</p>

### Jelaskan menggunakan visualisasi (gambar dengan pensil/ballpoint kemudian difoto), mengapa terjadi deadlock.

<img width="1200" height="1600" alt="24_deadlock" src="https://github.com/user-attachments/assets/1820d75d-8a1b-4912-a465-bf465732649c" />


#### Pembahasan

<p align="justify">Diagram menjelaskan terjadinya deadlock dalam empat tahap. Kondisi awal: lock_A dan lock_B belum terkunci. Thread 1 mengunci lock_A lalu mencoba mengunci lock_B, tetapi lock_B sedang dipegang Thread 2. Thread 2 mengunci lock_B lalu mencoba mengunci lock_A, tetapi lock_A sedang dipegang Thread 1. Pada tahap akhir terbentuk lingkaran saling menunggu (circular wait): Thread 1 memegang A dan menunggu B, Thread 2 memegang B dan menunggu A, sehingga keduanya tidak bisa melanjutkan.</p>

Berikut adalah contoh program untuk membuat supaya deadlock tersebut tidak terjadi (`deadlock-02.py`):

<img width="218" height="374" alt="25_deadlock-02 py" src="https://github.com/user-attachments/assets/308b84a1-26b7-43c9-a233-99d6e39b7a30" />

#### Pembahasan

<p align="justify">Ini versi perbaikan dengan acquire(timeout=5) dan blok try/finally. Thread tidak menunggu lock selamanya, dan setiap lock yang dipegang dilepas dengan release(). Kuncinya, Thread 1 melepas lock A sebelum mencoba mengambil lock B (begitu juga Thread 2), sehingga tidak ada thread yang memegang satu lock sambil menunggu lock lain, dan lingkaran saling menunggu tidak terbentuk.</p>

**Tugas:**

### -Jalankan program tersebut.

<img width="341" height="89" alt="26_Output_deadlock-02 py" src="https://github.com/user-attachments/assets/a915f7f5-3942-4e82-87aa-c5b95a47b1af" />

#### Pembahasan

<p align="justify">Kedua thread berhasil mengambil lock pertamanya (Thread 1 lock A, Thread 2 lock B), lalu masing-masing menunggu lock berikutnya. Karena lock pertama sudah dilepas, Thread 2 berhasil mengambil lock A dan Thread 1 berhasil mengambil lock B, lalu program selesai dengan “Execution Finished”. Deadlock teratasi dan program tidak hang.</p>

### -Amati keluarannya. Jelaskan mengapa deadlock tidak terjadi?
<p align="justify">Deadlock tidak terjadi karena setiap thread melepas lock pertamanya sebelum meminta lock kedua. Pada blok finally, Thread 1 menjalankan lock_a.release() dan Thread 2 menjalankan lock_b.release() sebelum keduanya memanggil acquire untuk lock berikutnya, sehingga tidak ada thread yang memegang satu lock sambil menunggu lock lain (tidak ada hold and wait maupun circular wait). Karena itu, Thread 2 bisa mendapat Lock A dan Thread 1 bisa mendapat Lock B, lalu program selesai dengan mencetak “Execution Finished”. Parameter timeout=5 juga berfungsi sebagai pengaman agar thread tidak menunggu selamanya, meskipun pada kasus ini tidak sempat terpakai.</p>
   

---

## 4 Algoritma Raft

Algoritma Raft banyak digunakan pada sistem terdistribusi, antara lain digunakan untuk mencapai konsensus. Berikut adalah simulasi algoritma Raft menggunakan Python yang diambil dari <https://www.c-sharpcorner.com/article/simulate-distributed-consensus-with-the-raft-protocol-simplified-using-python/>.

Class raft.py

<img width="329" height="445" alt="27_raft py" src="https://github.com/user-attachments/assets/1ab3a9b2-ecad-47b1-860c-ab90bfaa5cf8" />

<img width="397" height="399" alt="28_raft py" src="https://github.com/user-attachments/assets/41e1b752-1b40-4e78-8384-68ffe4d1b4c4" />


#### Pembahasan

<p align="justify">Program ini mensimulasikan konsensus Raft yang disederhanakan dengan tiga peran node, yaitu FOLLOWER, CANDIDATE, dan LEADER. Kelas RaftNode menyimpan term, log, dan waktu heartbeat, serta memiliki election_timeout acak 1 sampai 2 detik. Metode start_election() menaikkan term lalu menjadikan node sebagai leader jika suara cukup (disederhanakan: semua node dianggap memberi suara), on_heartbeat() mengembalikan node menjadi follower, append_entry() menambah log khusus leader, dan tick() memicu pemilihan jika heartbeat terlewat. Fungsi simulate_raft() menjalankan 3 node selama 20 langkah, dengan leader mengirim heartbeat dan menambah perintah setiap 3 langkah.</p>


### -Jalankan program tersebut.

<img width="305" height="439" alt="29_Output_raft py" src="https://github.com/user-attachments/assets/2a049d92-d6f2-47fa-81ec-4dfb5317710f" />

<img width="289" height="403" alt="30_Output_raft py" src="https://github.com/user-attachments/assets/7a7df193-93b5-4826-921d-777cb45da769" />

#### Pembahasan

<p align="justify">Pada step 1-2 semua node FOLLOWER dengan term 0 dan log kosong. Pada step 3, Node 2 terpilih menjadi LEADER di term 1 (karena timeout-nya habis lebih dulu). Setelah itu Node 1 dan 3 ikut ke term 1 melalui heartbeat dan tetap FOLLOWER. Leader menambah perintah di step 4, 7, 10, 13, 16, dan 19 (kelipatan 3), sehingga log Node 2 bertambah sampai 6 entri. Perlu dicatat, log Node 1 dan 3 tetap 0 karena replikasi log ke follower tidak diimplementasikan (hanya disimulasikan lewat komentar di kode). Term tetap 1 dan tidak ada pemilihan ulang, artinya sistem stabil.</p>


### -Perhatikan keluaran program yang dijalankan tersebut. Dari keluaran program tersebut, jelaskan secara sederhana algoritma Raft untuk memilih koordinator (LEADER) menggunakan visualisasi (digambar dengan manual pensil/ballpoint dan kemudian difoto).

<img width="720" height="1280" alt="31_LEADER" src="https://github.com/user-attachments/assets/5b8f4626-2d8c-45a2-b499-047a4d6f99de" />

#### Pembahasan

<p align="justify">Diagram menjelaskan simulasi dalam empat tahap: (1) kondisi awal step 1-2, semua node follower dan belum ada leader; (2) pemilihan leader step 3-5, node dengan suara terbanyak menjadi leader; (3) replikasi log step 4-5, leader mengirim entri ke follower; (4) operasi dan stabilitas step 6-20, leader tetap memimpin. Namun, ada ketidaksesuaian dengan output: pada diagram leader digambarkan Node 1, sedangkan pada output leader-nya adalah Node 2. Replikasi log pada tahap 3 juga tidak benar-benar terjadi di kode, karena log follower tetap 0.</p>

### -Buatlah program tersebut menjadi modul Python dan kemudian buatlah contoh simulasinya menggunakan modul Python yang sudah Anda buat tersebut.

Class main2.py

<img width="267" height="449" alt="32_main2 py" src="https://github.com/user-attachments/assets/e505da5b-dec3-4332-94ae-84e49b73da65" />

#### Pembahasan

<p align="justify">Ini versi modular yang mengimpor RaftNode dan State dari raft.py. Simulasinya sama (3 node, 20 langkah), tetapi ada beberapa perbedaan: leader dipilih dengan leaders[0] (bukan acak), leader menambah perintah setiap 5 langkah (step % 5 == 0, bukan 3), dan status yang dicetak menampilkan isi log (node.log), bukan hanya panjangnya. Selain itu, agar tidak mencetak ulang simulasi bawaan, file raft.py memang menjaga simulate_raft() di dalam if __name__ == "__main__".</p>

### -Output

<img width="311" height="415" alt="33_output_main py" src="https://github.com/user-attachments/assets/41abcf56-25c7-4814-bfe4-ad12b009a652" />

<img width="308" height="398" alt="34_output_main py" src="https://github.com/user-attachments/assets/7c5a101d-4138-40fe-a5e5-ba33e9ab5c1c" />

#### Pembahasan

<p align="justify">Pada step 1-2 semua node masih FOLLOWER dengan term 0. Di step 3, Node 2 terpilih menjadi LEADER di term 1, lalu Node 1 dan 3 ikut term 1 lewat heartbeat dan tetap FOLLOWER. Leader menambah perintah setiap kelipatan 5 langkah (command-5, command-10, command-15), sehingga log Node 2 berisi tiga entri, sedangkan log Node 1 dan 3 tetap kosong karena replikasi log tidak diimplementasikan. Term tetap 1 dan tidak ada pemilihan ulang, artinya sistem stabil.</p>

  

# KESIMPULAN

<p align="justify">Berdasarkan praktikum ini, dapat disimpulkan bahwa sistem terdistribusi dan terdesentralisasi menghadapi tantangan koordinasi karena tidak adanya jam global maupun kontrol terpusat. Vector clock terbukti mampu menentukan urutan kejadian antar proses (happens-before) dan mengidentifikasi kejadian yang konkuren tanpa bergantung pada jam global. Pada eksekusi konkuren, race condition terjadi ketika beberapa thread mengubah data bersama tanpa sinkronisasi (saldo menjadi Rp-60) dan dapat diatasi dengan threading.Lock(), sedangkan deadlock terjadi ketika dua thread saling menunggu lock yang dipegang lawannya dan dapat dicegah dengan timeout, pelepasan lock sebelum mengambil lock lain, atau urutan pengambilan lock yang konsisten. Terakhir, simulasi algoritma Raft menunjukkan bahwa node-node dapat mencapai konsensus dan memilih satu leader secara terdesentralisasi melalui election timeout acak dan heartbeat, sehingga sistem tetap stabil dengan satu leader yang mengoordinasikan perintah, meskipun replikasi log ke follower pada simulasi ini masih disederhanakan.</p>
