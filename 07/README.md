# Praktikum Minggu MODUL 07 - Cloud Computing


| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi | 
| **Topik** | Cloud Computing |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 | 
| **Kelas** | IF-1 |

---

#  TUJUAN PRAKTIKUM

---
#  DASAR TEORI

---
#  PEMBAHASAN
### source

### 1. Membuat env Python 3.14.4

Salin satu persatu kode dibawah ini:

```python
uv python install 3.14.4
uv venv --python 3.14.4
.venv\Scripts\activate.bat
python --version
```

<img width="522" height="163" alt="03" src="https://github.com/user-attachments/assets/080bd638-2eec-46d4-909e-cff2973c3fb3" />

#### Pembahasan

<p align="justify">Perintah-perintah di terminal ini berhasil menyiapkan lingkungan Python 3.14.4 untuk proyek flask-app Anda menggunakan uv: uv python install 3.14.4 memastikan Python versi tersebut sudah terpasang (hasilnya “already installed”, jadi tidak perlu mengunduh ulang), lalu uv venv --python 3.14.4 membuat virtual environment di folder .venv, dan karena folder tersebut sudah ada, uv menanyakan apakah ingin menggantinya dan Anda menjawab “yes” sehingga .venv lama dibuat ulang dari awal. Setelah itu, .venv\Scripts\activate.bat mengaktifkan environment tersebut (ditandai prefiks (flask-app) di prompt), dan python --version mengonfirmasi bahwa Python yang aktif adalah 3.14.4, artinya environment sudah siap dipakai untuk menginstal dependensi seperti Flask dengan uv pip install flask.</p>


### 2. Install Paket yang Diperlukan

```python
uv pip install -e .
```

<img width="419" height="158" alt="04_uv_pip_install" src="https://github.com/user-attachments/assets/c366c1ca-2ee7-4965-8936-f1d14c053c01" />

#### Pembahasan

<p align="justify">Perintah uv pip install -e . berhasil memasang proyek flaskr Anda dalam mode editable (-e), artinya paket dipasang sebagai tautan ke folder proyek sehingga setiap perubahan pada kode langsung berlaku tanpa perlu instal ulang. uv me-resolve 8 paket dalam 2,27 detik, membangun flaskr versi 1.0.0 dari folder lokal, lalu memasang semuanya dalam 157 ms: selain flaskr sendiri, terpasang flask 3.1.3 beserta dependensinya, yaitu werkzeug (penangan WSGI dan routing), jinja2 (mesin template), click (antarmuka perintah CLI), itsdangerous (penandatanganan data seperti session), markupsafe (pengamanan teks pada template), dan blinker (sistem sinyal/event). Dengan begitu, aplikasi Flask Anda sudah siap dijalankan, misalnya dengan flask --app flaskr run --debug.</p>

```python
flask --app flaskr init-db
flask --app flaskr run
```

<img width="725" height="97" alt="05_flask" src="https://github.com/user-attachments/assets/201dd2a5-3a7a-4116-9ec5-bd795ef16741" />

#### Pembahasan

<p align="justify">Perintah flask --app flaskr init-db berhasil membuat dan menginisialisasi database aplikasi (ditandai pesan “Initialized the database”), biasanya dengan menjalankan skema SQL yang menghasilkan file SQLite di folder instance. Setelah itu, flask --app flaskr run menjalankan aplikasi flaskr pada server pengembangan bawaan Flask yang dapat diakses di http://127.0.0.1:5000 (localhost, port 5000), sehingga Anda bisa membukanya lewat browser. Pesan Debug mode: off berarti mode debug tidak aktif, jadi server tidak akan memuat ulang otomatis saat kode diubah dan tidak menampilkan debugger interaktif jika terjadi error; untuk pengembangan, tambahkan --debug. Peringatan berwarna merah hanyalah pengingat bahwa server ini khusus untuk pengembangan, bukan untuk produksi, yang seharusnya memakai server WSGI seperti Gunicorn atau Waitress.</p>

<img width="463" height="215" alt="06_Register" src="https://github.com/user-attachments/assets/2ceee64f-b120-4c8d-8ea8-0870ae772540" />

#### Pembahasan

<img width="468" height="233" alt="07_Login" src="https://github.com/user-attachments/assets/149d4521-c970-47f7-9156-9f0f3dce5861" />

#### Pembahasan

<img width="464" height="103" alt="08_Hasil" src="https://github.com/user-attachments/assets/21927787-bee2-465c-90ee-771778777ad2" />

#### Pembahasan

<img width="714" height="300" alt="09_Hasil_tes_lokal" src="https://github.com/user-attachments/assets/c11b8933-41cb-4bc0-9e3d-a274b1626c91" />

#### Pembahasan

### 3. Buat Aplikasi Menjadi CA - Docker

Buat Dockerfile

```python
(
echo FROM python:3.14
echo.
echo RUN mkdir /app
echo WORKDIR /app
echo ADD . /app/
echo RUN pip install -e .
echo RUN flask --app flaskr init-db
echo.
echo EXPOSE 5000
echo CMD ["flask", "--app", "flaskr", "run", "--host=0.0.0.0", "--port=5000"]
) > Dockerfile
```

<img width="516" height="149" alt="10_Buat_Dockerfile" src="https://github.com/user-attachments/assets/ea31eeaa-b072-4848-92e0-f807c1b7c748" />

#### Pembahasan

Buat .dockerignore, supaya .venv Windows tidak ikut masuk ke image Linux:

```python
(
echo .venv
echo __pycache__
echo instance
echo *.pyc
) > .dockerignore
```

<img width="372" height="84" alt="11_Buat_dockerignore" src="https://github.com/user-attachments/assets/6f6760f7-8eaf-4f4c-91fa-14be85090911" />

#### Pembahasan

Cek isinya

```python
type Dockerfile
```

<img width="447" height="139" alt="12_Cek_Isi" src="https://github.com/user-attachments/assets/7c3f2221-8669-4084-a701-6a8dac8cd246" />

#### Pembahasan

Build dan cek image

```python
docker build -f Dockerfile -t flaskr:1.0.0 .
docker image ls
```

<img width="469" height="290" alt="13_Build" src="https://github.com/user-attachments/assets/6f5e70cb-ce54-40c6-a05b-090caddab88f" />

#### Pembahasan

<img width="472" height="131" alt="14_Cek_Image" src="https://github.com/user-attachments/assets/506c0d48-ad76-41c3-b743-36ed79340b59" />

#### Pembahasan

### 4. Menjalankan Image

```python
docker run -p 5001:5000 flaskr:1.0.0
```

<img width="716" height="141" alt="15_jalankan" src="https://github.com/user-attachments/assets/ee3a4215-e495-4121-b6e3-f6be0b2f85f3" />

#### Pembahasan

<img width="464" height="102" alt="16_Tampilan_hasil" src="https://github.com/user-attachments/assets/22bb2240-b86d-4188-a7d1-205aa498bf65" />

#### Pembahasan

### 5. Buat Aplikasi Menjadi CA - Podman
Podman

```python
winget install --id RedHat.Podman -e
```

<img width="461" height="122" alt="17_Podman" src="https://github.com/user-attachments/assets/f294ff80-3424-48b7-a7c3-1d7b51bab855" />

#### Pembahasan

```python
podman build -f Dockerfile -t flaskr:1.0.0 .
```

<img width="779" height="453" alt="18" src="https://github.com/user-attachments/assets/530943e2-8884-4daa-950d-173ba734cabd" />

<img width="956" height="339" alt="19" src="https://github.com/user-attachments/assets/982a8bee-17d1-4a18-a8ab-f808ca92c7e2" />

#### Pembahasan

```python
podman image ls
```

<img width="494" height="81" alt="20" src="https://github.com/user-attachments/assets/32cffcdd-b597-4469-8cee-9b2a122f170c" />

#### Pembahasan

```python
podman run -p 5001:5000 flaskr:1.0.0
```

<img width="713" height="116" alt="21" src="https://github.com/user-attachments/assets/236063e8-5ae9-4a98-b840-21f0fcad7b26" />

#### Pembahasan

Buka http://127.0.0.1:5001. Jika Podman menanyakan registry untuk python:3.14, pilih docker.io.

<img width="472" height="106" alt="22" src="https://github.com/user-attachments/assets/a615ea9e-0ab7-414d-aae1-0e18a728697d" />

#### Pembahasan

<img width="717" height="170" alt="23" src="https://github.com/user-attachments/assets/5161585b-3d6b-4163-94b5-cf7b6bcbce38" />

#### Pembahasan


---
# KESIMPULAN

---
# REFERENSI
