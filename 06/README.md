# Praktikum Minggu MODUL 04 - Konsistensi dan Replikasi pada Sistem Terdistribusi

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
JDK 17, pdsh, ssh, dan sshd dibutuhkan. Di Ubuntu, sshd dijalankan dengan service (ini pengganti dinitctl/systemctl di modul).
<img width="679" height="386" alt="01-instalasi-java-17-ubuntu-wsl" src="https://github.com/user-attachments/assets/3feef7ed-7403-40ef-830c-b87411678160" />
<img width="812" height="419" alt="02-instalasi-java-17-ubuntu-wsl" src="https://github.com/user-attachments/assets/127673e6-1685-4572-83e6-ca0530e8a5ce" />
#### Pembahasan
<p align="justify">Kedua gambar menunjukkan bahwa kendala yang muncul di CMD sebelumnya sudah teratasi setelah perintah dijalankan di Ubuntu lewat WSL. Prosesnya dimulai dengan masuk ke Ubuntu menggunakan wsl -d Ubuntu, lalu menjalankan sudo apt update untuk memperbarui daftar paket, yang menunjukkan ada 147 paket yang bisa di-upgrade. Setelah itu, perintah sudo apt install -y openjdk-17-jdk pdsh openssh-server openssh-client dijalankan. Hasilnya, pdsh, openssh-server, dan openssh-client ternyata sudah terpasang dengan versi terbaru, sehingga hanya paket OpenJDK 17 (jdk, jdk-headless, jre, dan jre-headless) yang diunduh sebesar 122 MB dan di-upgrade dari versi 17.0.20 ke 17.0.21. Setelah instalasi selesai, sudo service ssh start berjalan tanpa error, dan java -version kini menampilkan OpenJDK 17.0.21 (build 2026-10-24). Dengan demikian, syarat utama untuk menjalankan Hadoop, yaitu Java 17 dan SSH, sudah terpenuhi. Langkah berikutnya adalah membuat folder kerja dengan mkdir -p ~/master/data-engineering/apache-hadoop, masuk ke folder tersebut dengan cd, lalu mengunduh Hadoop 3.5.0 dengan wget, yang kini bisa berjalan normal karena sudah berada di lingkungan Linux.</p>

## 1 Unduh Apache Hadoop
##
##
##
##
##
##
##
##
##
##
##

#  TUGAS

---
# KESIMPULAN

---
# REFERENSI

