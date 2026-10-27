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

#### Jalankan primary dan replica
```python
docker compose up -d
```

#### Periksa container
```python
docker ps
```

#### Periksa log jika terjadi masalah
```python
docker compose logs postgres_primary
```

```python
docker compose logs postgres_replica
```

#### - Jalankan kode dibawah jika ingin menghentikan container
```python
docker compose down
```


  



  

# KESIMPULAN
