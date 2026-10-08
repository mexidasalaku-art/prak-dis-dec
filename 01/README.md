# Praktikum Minggu 1
# Nama  : Yesaya Mexi Dasalaku
# NIM   : 255410029
# Kelas : IF-1
# Bab 1: Instalasi Git

## Tujuan

- Mengunduh dan memasang Git for Windows.
- Memilih pengaturan installer yang tepat.
- Memverifikasi bahwa Git berjalan.

## Langkah-langkah

1. Buka <https://git-scm.com/downloads/win> di browser, lalu unduh installer **64-bit Git for Windows Setup**.

   ![Halaman unduhan Git for Windows](images/install-git-01.png)

2. Jalankan file installer yang sudah diunduh. Jika Windows menanyakan izin, klik **Yes**.

3. Pada halaman lisensi, klik **Next**. Pada halaman lokasi instalasi, biarkan bawaan lalu klik **Next**.

4. Pada halaman **Select Components**, biarkan pilihan bawaan lalu klik **Next**. Anda juga boleh mencentang **Add a Git Bash Profile to Windows Terminal** jika memakai Windows Terminal.

   ![Memilih komponen instalasi](images/install-git-02.png)

5. Pilih editor yang akan digunakan bersama Git. Pada dasarnya Anda bebas memilih editor apa pun. Vim sulit dipakai pemula, jadi pilih **Use Visual Studio Code as Git's default editor** jika VS Code sudah terpasang. Jika belum, pilih editor lain seperti Notepad++.

   ![Memilih editor default Git](images/install-git-03.png)

6. Pada halaman **Adjusting the name of the initial branch**, pilih **Override the default branch name for new repositories** dan isi `main`. Ini sesuai dengan nama branch awal di GitHub.

   ![Menentukan nama branch awal](images/install-git-04.png)

7. Pada halaman **Adjusting your PATH environment**, pilih **Git from the command line and also from 3rd-party software**. Pilihan ini membuat perintah `git` bisa dipakai dari Command Prompt dan PowerShell.

   ![Memilih pengaturan PATH](images/install-git-05.png)

8. Pada halaman berikutnya, biarkan pilihan bawaan untuk SSH, HTTPS transport backend, line ending, dan terminal emulator. Klik **Next** di setiap halaman.

9. Pada halaman **Choose a credential helper**, biarkan **Git Credential Manager**. Fitur ini yang membuka jendela login GitHub saat Anda melakukan push pertama.

10. Klik **Install** dan tunggu sampai selesai, lalu klik **Finish**.

    ![Instalasi selesai](images/install-git-06.png)

## Verifikasi

Buka **Command Prompt** (tekan tombol Windows, ketik `cmd`, lalu Enter) dan jalankan:

```
git --version
<img width="251" height="42" alt="image" src="https://github.com/user-attachments/assets/c74436b8-fa72-4d8e-b80b-ce746756318d" />


Hasil yang diharapkan berupa nomor versi, misalnya:

```
git version 2.56.0.windows.2
```

Jika Anda menjalankan `git` saja, yang muncul adalah daftar bantuan perintah. Itu juga menandakan Git sudah terpasang.

![Hasil git --version di Command Prompt](images/install-git-07.png)

## Masalah yang sering muncul

| Gejala | Penyebab | Solusi |
| --- | --- | --- |
| `'git' is not recognized` | Terminal dibuka sebelum instalasi selesai, atau PATH belum diatur | Tutup dan buka kembali terminal. Jika masih gagal, pasang ulang dan pilih opsi PATH pada langkah 7 |
| Installer tidak mau berjalan | Izin administrator ditolak | Jalankan ulang installer dan klik **Yes** saat diminta izin |

## Latihan

- [ ] Jalankan `git --version` dan tangkap layar hasilnya.
- [ ] Jalankan `git help commit` dan lihat halaman bantuan yang terbuka di browser.
- [ ] Sebutkan editor yang Anda pilih pada langkah 5 beserta alasannya.
