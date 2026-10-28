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

### 4.2 Replikasi Master-Master Menggunakan Apache Ignite 3

#### Struktur Direktori dan File

<img width="131" height="191" alt="28_Direktori_dan_file" src="https://github.com/user-attachments/assets/e53b62ad-06e1-4c25-88a1-7a55e31765b4" />

#### Pembahasan




  

# KESIMPULAN
# REFERENSI
