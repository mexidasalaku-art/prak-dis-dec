<div align="center">

# 📘 Petunjuk Penggunaan Git dan GitHub

**Panduan praktis mengelola laporan, kode, dan foto praktikum secara terstruktur**

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Markdown](https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)

</div>

---

| | |
|---|---|
| **Penulis** | Yesaya Mexi Dasalaku |
| **Peran** | Penulis |
| **Pembaruan Terakhir** | 10 Oktober 2026 |

Dokumen ini menjelaskan cara menggunakan Git dan GitHub untuk mengelola dokumen digital, menyimpan kode program, membuat folder tugas, mengunggah foto praktikum, dan mengelola laporan secara terstruktur.

Modul ini disusun untuk membantu mahasiswa memahami penggunaan Git dan GitHub dalam kegiatan praktikum dan pengerjaan tugas perkuliahan.

---

## 📑 Daftar Isi

1. [Pengenalan Git dan GitHub](#1-pengenalan-git-dan-github)
2. [Instalasi Git](#2-instalasi-git)
3. [Konfigurasi Git](#3-konfigurasi-git)
4. [Membuat Repository GitHub](#4-membuat-repository-github)
5. [Membuat Folder dan File](#5-membuat-folder-dan-file)
6. [Mengunggah Laporan dan Foto](#6-mengunggah-laporan-dan-foto)
7. [Mengelola Perubahan File](#7-mengelola-perubahan-file)
8. [Kesimpulan](#8-kesimpulan)

---

## 1. Pengenalan Git dan GitHub

| | Penjelasan |
|---|---|
| **Git** | Sistem pengontrol versi yang digunakan untuk mencatat perubahan pada file dan kode program. |
| **GitHub** | Platform online untuk menyimpan repository, mengelola proyek, dan berbagi pekerjaan dengan orang lain. |

**Tujuan penggunaan Git dan GitHub:**

- ☁️ Menyimpan file tugas secara online.
- 📝 Mengelola perubahan dokumen.
- 🗂️ Memisahkan laporan dan foto dalam folder.
- 📤 Mempermudah pengumpulan tugas kepada dosen.

---

## 2. Instalasi Git

1. Buka website [https://git-scm.com/](https://git-scm.com/).
2. Unduh Git sesuai sistem operasi komputer.
3. Jalankan file installer.
4. Ikuti petunjuk instalasi hingga selesai.
5. Buka **Command Prompt** atau **Terminal**.
6. Ketik perintah berikut untuk memeriksa instalasi:

```bash
git --version
```

> [!NOTE]
> Jika versi Git muncul (misalnya `git version 2.x.x`), instalasi berhasil.

---

## 3. Konfigurasi Git

Setelah Git terpasang, lakukan konfigurasi nama dan email. Buka terminal, kemudian masukkan perintah:

```bash
git config --global user.name "Nama Mahasiswa"
git config --global user.email "email@example.com"
```

> [!TIP]
> Ganti nama dan email di atas dengan identitas yang kamu gunakan untuk Git (sebaiknya sama dengan email akun GitHub).

---

## 4. Membuat Repository GitHub

1. Buka [https://github.com/](https://github.com/).
2. Login ke akun GitHub.
3. Klik tombol **+**, kemudian pilih **New repository**.
4. Masukkan nama repository, misalnya `praktikum-komputer`.
5. Pilih **Public** atau **Private** sesuai kebutuhan.
6. Klik **Create repository**.

Repository digunakan sebagai tempat penyimpanan file tugas dan dokumentasi praktikum.

---

## 5. Membuat Folder dan File

Agar file tersusun rapi, buat folder berdasarkan nomor praktikum.

**Contoh struktur repository:**

```text
praktikum-komputer/
├── README.md
├── 01/
    ├── README.md
    └── Images/
        ├── foto1.png
        └── foto2.png

```

**Keterangan:**

| Item | Fungsi |
|---|---|
| `README.md` | Berisi penjelasan utama repository atau laporan. |
| `01/`, `02/` | Folder untuk memisahkan setiap praktikum. |
| `Images/` | Folder untuk menyimpan foto dokumentasi. |
| `foto1.png`, `foto2.png` | File foto disimpan sesuai kegiatan praktikum. |

---

## 6. Mengunggah Laporan dan Foto

Langkah-langkah mengunggah file melalui website GitHub:

1. Buka repository yang ingin digunakan.
2. Masuk ke folder tujuan.
3. Klik **Add file**.
4. Pilih **Upload files**.
5. Pilih file laporan atau foto dari komputer.
6. Klik **Commit changes** untuk menyimpan perubahan.

**Format file yang didukung:**

| Jenis | Format |
|---|---|
| Laporan | `PDF`, `DOCX`, atau `Markdown` |
| Foto | `JPG` atau `PNG` |

> [!IMPORTANT]
> Pastikan laporan dan foto dimasukkan ke folder yang sesuai.

**Menampilkan foto di dalam laporan (`README.md`):**

```markdown
![Deskripsi foto](Images/foto1.png)
```

---

## 7. Mengelola Perubahan File

Jika ingin memperbarui laporan:

1. Buka file laporan pada repository.
2. Klik ikon pensil ✏️ atau **Edit** jika tersedia.
3. Lakukan perubahan.
4. Klik **Commit changes**.

> [!NOTE]
> Setiap perubahan yang disimpan akan tercatat dalam riwayat repository (*commit history*), sehingga kamu dapat melihat perkembangan file.

---

## 8. Kesimpulan

Git dan GitHub membantu mahasiswa menyimpan, mengatur, serta memperbarui file praktikum secara terstruktur. Dengan membuat folder terpisah untuk laporan dan foto, dokumen menjadi lebih mudah ditemukan dan diperiksa. Penggunaan repository juga mempermudah pengumpulan serta dokumentasi tugas perkuliahan.

---

<div align="center">

*Terakhir diperbarui: 10 Oktober 2026*

</div>
