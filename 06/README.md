
| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi | 
| **Topik** | Konsistensi dan Replikasi pada Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 | 
| **Kelas** | IF-1 |

---

#  TUJUAN PRAKTIKUM


---
#  DASAR TEORI
---

#  PEMBAHASAN PRAKTIK
## Persyaratan software

```python
sudo apt update
sudo apt install -y openjdk-17-jdk pdsh openssh-server openssh-client
sudo service ssh start
java -version
```

JDK 17, pdsh, ssh, dan sshd dibutuhkan. Di Ubuntu, sshd dijalankan dengan service (ini pengganti dinitctl/systemctl di modul).

<img width="679" height="386" alt="01-instalasi-java-17-ubuntu-wsl" src="https://github.com/user-attachments/assets/3feef7ed-7403-40ef-830c-b87411678160" />
<img width="812" height="419" alt="02-instalasi-java-17-ubuntu-wsl" src="https://github.com/user-attachments/assets/127673e6-1685-4572-83e6-ca0530e8a5ce" />
#### Pembahasan

<p align="justify">Kedua gambar menunjukkan bahwa kendala yang muncul di CMD sebelumnya sudah teratasi setelah perintah dijalankan di Ubuntu lewat WSL. Prosesnya dimulai dengan masuk ke Ubuntu menggunakan wsl -d Ubuntu, lalu menjalankan sudo apt update untuk memperbarui daftar paket, yang menunjukkan ada 147 paket yang bisa di-upgrade. Setelah itu, perintah sudo apt install -y openjdk-17-jdk pdsh openssh-server openssh-client dijalankan. Hasilnya, pdsh, openssh-server, dan openssh-client ternyata sudah terpasang dengan versi terbaru, sehingga hanya paket OpenJDK 17 (jdk, jdk-headless, jre, dan jre-headless) yang diunduh sebesar 122 MB dan di-upgrade dari versi 17.0.20 ke 17.0.21. Setelah instalasi selesai, sudo service ssh start berjalan tanpa error, dan java -version kini menampilkan OpenJDK 17.0.21 (build 2026-10-24). Dengan demikian, syarat utama untuk menjalankan Hadoop, yaitu Java 17 dan SSH, sudah terpenuhi. Langkah berikutnya adalah membuat folder kerja dengan mkdir -p ~/master/data-engineering/apache-hadoop, masuk ke folder tersebut dengan cd, lalu mengunduh Hadoop 3.5.0 dengan wget, yang kini bisa berjalan normal karena sudah berada di lingkungan Linux.</p>

## 1. Unduh Apache Hadoop

```python
mkdir -p ~/master/data-engineering/apache-hadoop
cd ~/master/data-engineering/apache-hadoop
wget https://archive.apache.org/dist/hadoop/common/hadoop-3.5.0/hadoop-3.5.0.tar.gz
```

<img width="889" height="185" alt="03" src="https://github.com/user-attachments/assets/02df18c6-ccc1-4b27-abae-88bc30175551" />

#### Pembahasan

<img width="917" height="409" alt="04" src="https://github.com/user-attachments/assets/db8b5826-ba91-4bd2-85f6-1ff9fa652899" />

#### Pembahasan



## 2. Instalasi Apache Hadoop

<img width="666" height="466" alt="05" src="https://github.com/user-attachments/assets/4c93a81f-c007-43ad-bc22-6123475b03c2" />
<img width="565" height="342" alt="06" src="https://github.com/user-attachments/assets/de87a080-22e5-4636-a091-00475bb358bf" />

#### Pembahasan

<p align="justify">Pada tahap ini dilakukan konfigurasi awal Apache Hadoop versi 3.5.0 pada Ubuntu melalui terminal. Proses dimulai dengan membuat symbolic link bernama hadoop, kemudian membuat direktori penyimpanan konfigurasi environment dan mengatur variabel HADOOP_HOME serta PATH agar perintah Hadoop dapat dijalankan melalui terminal. Setelah itu, perintah source digunakan untuk memuat konfigurasi tersebut. Ketika perintah hadoop dijalankan, terminal menampilkan daftar perintah dan opsi Hadoop. Namun, masih terdapat peringatan pada konfigurasi here-document yang perlu diperbaiki agar pengaturan environment dapat diterapkan dengan benar.</p>

## 3. engaturan pdsh dan SSH tanpa password

## 4. Konfigurasi Hadoop
## 5. Format NameNode
## 6. Atur JAVA_HOME
## 7. Jalankan daemon HDFS
## 8 
## 9
## 10
##
##

#  TUGAS

---
# KESIMPULAN

---
# REFERENSI

