# Praktikum Minggu MODUL 04 - Konsistensi dan Replikasi pada Sistem Terdistribusi

| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi |
| **Topik** | Konsistensi dan Replikasi pada Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 | 
| **Kelas** | IF-1 |

---

##  TUJUAN PRAKTIKUM

---

##  DASAR TEORI

---


#  PEMBAHASAN
### 4.1 Streaming Replication Menggunakan PostgreSQL
### Install Docker
- Langkah-langkah Instal Docker 

<img width="402" height="290" alt="01" src="https://github.com/user-attachments/assets/4405358d-e059-4042-8329-da70aacbdf25" />

#### Pembahasan


<img width="527" height="364" alt="02" src="https://github.com/user-attachments/assets/27fd860d-5c9d-455b-9fe5-1c747adb7f8c" />

#### Pembahasan

<img width="531" height="362" alt="03" src="https://github.com/user-attachments/assets/8f29d8d0-75e8-414c-b127-1d5160daa9fa" />

#### Pembahasan

---
### Pemeriksaan Versi dan Lingkungan
- versi Docker & Compose
#### Docker Version

<img width="270" height="35" alt="04" src="https://github.com/user-attachments/assets/f66b43ae-4b7d-4654-8bdc-181f1f9cb8e9" />

#### Pembahasan

#### Docker Compose Version

<img width="258" height="40" alt="05" src="https://github.com/user-attachments/assets/6e7f19c9-02e5-49bc-bb2c-87b4c9a118a1" />

#### Pembahasan

#### Docker info

<img width="269" height="347" alt="06" src="https://github.com/user-attachments/assets/54ecff99-f590-43c0-974a-c2d923deeacc" />


#### Pembahasan

### Struktur Direktori dan FIle

<img width="218" height="92" alt="07" src="https://github.com/user-attachments/assets/6705cff0-522f-485f-a9c8-58871c50c0fe" />

#### Pembahasan


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

```python
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ignite3-node1-1
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ignite3-node2-1
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ignite3-node3-1
```

<img width="689" height="90" alt="32_alamat_IP_node" src="https://github.com/user-attachments/assets/20535869-2b35-4c93-a876-0c06d7b25997" />

#### Pembahasan


  

# KESIMPULAN
# REFERENSI
