# Praktikum Minggu MODUL 06 - Distributed File System - HDFS

| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi | 
| **Topik** | Distributed File System - HDFS |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 | 
| **Kelas** | IF-1 |

---

#  TUJUAN PRAKTIKUM


---
#  DASAR TEORI
---

#  PEMBAHASAN
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

<p align="justify">Pada tahap ini dilakukan pencarian dan pemilihan versi Apache Hadoop melalui website resmi Apache Hadoop. Berdasarkan tampilan halaman download, versi yang digunakan adalah Hadoop 3.5.0 dengan tanggal rilis 2 April 2026. Halaman tersebut menyediakan pilihan unduhan berupa source code dan binary download. Versi 3.5.0 dipilih sebagai perangkat lunak yang akan digunakan dalam praktikum pengolahan data terdistribusi.</p>

<img width="917" height="409" alt="04" src="https://github.com/user-attachments/assets/db8b5826-ba91-4bd2-85f6-1ff9fa652899" />

#### Pembahasan

<p align="justify">Pada tahap ini dilakukan pengunduhan file Apache Hadoop versi 3.5.0 melalui terminal Ubuntu menggunakan perintah wget dari server resmi Apache. File yang diunduh bernama hadoop-3.5.0.tar.gz dengan ukuran sekitar 554 MB. Proses pengunduhan berhasil diselesaikan hingga mencapai 100% dan menampilkan status saved, yang menunjukkan bahwa file Hadoop telah berhasil tersimpan dan siap digunakan untuk proses instalasi selanjutnya.</p>



## 2. Instalasi Apache Hadoop

<img width="666" height="466" alt="05" src="https://github.com/user-attachments/assets/4c93a81f-c007-43ad-bc22-6123475b03c2" />
<img width="565" height="342" alt="06" src="https://github.com/user-attachments/assets/de87a080-22e5-4636-a091-00475bb358bf" />

#### Pembahasan

<p align="justify">Pada tahap ini dilakukan konfigurasi awal Apache Hadoop versi 3.5.0 pada Ubuntu melalui terminal. Proses dimulai dengan membuat symbolic link bernama hadoop, kemudian membuat direktori penyimpanan konfigurasi environment dan mengatur variabel HADOOP_HOME serta PATH agar perintah Hadoop dapat dijalankan melalui terminal. Setelah itu, perintah source digunakan untuk memuat konfigurasi tersebut. Ketika perintah hadoop dijalankan, terminal menampilkan daftar perintah dan opsi Hadoop. Namun, masih terdapat peringatan pada konfigurasi here-document yang perlu diperbaiki agar pengaturan environment dapat diterapkan dengan benar.</p>

## 3. Pengaturan pdsh dan SSH tanpa password

<img width="496" height="431" alt="09" src="https://github.com/user-attachments/assets/7f900b42-f60a-49d0-b5fa-b6f97d15f48b" />

#### Pembahasan

<p align="justify">Pada tahap ini dilakukan konfigurasi SSH (Secure Shell) untuk Apache Hadoop agar komunikasi antarproses Hadoop dapat berjalan tanpa perlu memasukkan password secara berulang. Proses dimulai dengan membuat SSH key menggunakan perintah ssh-keygen, kemudian menambahkan public key ke file authorized_keys dan mengatur hak akses menggunakan perintah chmod 0600. Selanjutnya, dilakukan pengujian koneksi menggunakan perintah ssh localhost. Hasilnya menunjukkan pesan Welcome to Ubuntu 26.04.1 LTS, yang menandakan bahwa koneksi SSH ke localhost berhasil dilakukan tanpa memasukkan password.</p>


## 4. Konfigurasi Hadoop
<img width="639" height="469" alt="14-4" src="https://github.com/user-attachments/assets/0eb07402-05e2-49ca-b4e0-0c80cc5ed82e" />
<img width="797" height="186" alt="15-4" src="https://github.com/user-attachments/assets/ffdc2809-8654-4527-b8e1-d99296f5928a" />

#### Pembahasan

<p align="justify">Pada tahap ini dilakukan konfigurasi beberapa file XML Hadoop, yaitu hdfs-site.xml, core-site.xml, mapred-site.xml, dan yarn-site.xml menggunakan perintah cat. Konfigurasi tersebut bertujuan untuk mengatur replikasi HDFS, menentukan alamat NameNode pada localhost:9000, mengatur framework MapReduce menggunakan YARN, serta mengatur layanan dan kapasitas sumber daya NodeManager. Dengan konfigurasi ini, Hadoop dipersiapkan agar komponen HDFS, MapReduce, dan YARN dapat saling terhubung dan berjalan dengan baik.</p>


## 5. Format NameNode
<img width="457" height="77" alt="10-langkah-5" src="https://github.com/user-attachments/assets/9769e4b8-2c21-4582-94b9-ae92b6f06c23" />

#### Pembahasan

<p align="justify">Pada tahap ini dilakukan pemeriksaan versi Java menggunakan perintah java -version dan hasilnya menunjukkan bahwa OpenJDK 17 berhasil terpasang. Selanjutnya, perintah hdfs namenode -format dijalankan untuk memformat NameNode Hadoop, tetapi proses belum berhasil karena NameNode masih berjalan. Oleh karena itu, proses NameNode perlu dihentikan terlebih dahulu sebelum melakukan format ulang.</p>

## 6. Atur JAVA_HOME
<img width="464" height="38" alt="11_6" src="https://github.com/user-attachments/assets/cae6595f-b9fd-4b5a-a283-62ec56e9afe0" />

#### Pembahasan

<p align="justify">Pada tahap ini dilakukan pemeriksaan folder instalasi JDK menggunakan perintah ls /usr/lib/jvm/ untuk mengetahui lokasi Java OpenJDK yang tersedia. Selanjutnya, variabel JAVA_HOME ditambahkan ke file hadoop-env.sh menggunakan perintah echo agar Hadoop dapat mengenali lokasi instalasi Java sebagai lingkungan yang dibutuhkan untuk menjalankan Hadoop.</p>


## 7. Jalankan daemon HDFS
<img width="461" height="192" alt="12-7" src="https://github.com/user-attachments/assets/ca6ded01-708e-4526-a266-fe2373ff94b1" />

#### Pembahasan

<img width="659" height="457" alt="13-7" src="https://github.com/user-attachments/assets/5f5f3d12-c4fa-45ba-ac37-7864a6ca76ba" />

#### Pembahasan


---
#  TUGAS
## Contoh operasi dan TUGAS
<img width="391" height="91" alt="16-tugas" src="https://github.com/user-attachments/assets/bb1ba96e-2d48-40fc-9247-b46124dcd248" />

#### Pembahasan

## 1. Buat direktori datasets
<img width="307" height="29" alt="17_t1" src="https://github.com/user-attachments/assets/7830b731-3eb6-44a6-86a5-b4a15f6bcf32" />

#### Pembahasan

## 2. Unduh 3 CSV dan salin ke HDFS
<img width="569" height="469" alt="18" src="https://github.com/user-attachments/assets/36b05266-9f14-40d8-ad0a-b602b2593a18" />
<img width="480" height="116" alt="19-t2" src="https://github.com/user-attachments/assets/661b23cb-165b-484d-92bd-f43656462d44" />

#### Pembahasan

---
# KESIMPULAN

---
# REFERENSI

