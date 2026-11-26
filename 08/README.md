# Praktikum Minggu MODUL 08 - Arsitektur Microservices untuk Sistem Terdistribusi


| | |
| --- | --- |
| **Mata Kuliah** | Praktikum Sistem Terdistribusi dan Terdesentralisasi | 
| **Topik** | Arsitektur Microservices untuk Sistem Terdistribusi |
| **Nama** | Yesaya Mexi Dasalaku |
| **NIM** | 255410029 | 
| **Kelas** | IF-1 |

---

#  TUJUAN PRAKTIKUM


---
#  DASAR TEORI
### 1.1 Install uv

```python
winget install --id=astral-sh.uv -e
```
<img width="721" height="293" alt="01" src="https://github.com/user-attachments/assets/3d5cc144-aa21-44fe-8981-67f6305a1f95" />

#### Pembahasan

```python
uv --version
```

<img width="471" height="96" alt="02" src="https://github.com/user-attachments/assets/469200cc-bd48-41c8-9b8b-37ccf40f4353" />

#### Pembahasan

### 1.2 Buat workspace dan pin Python 3.14

```python
uv python install 3.14
uv python list
```

<img width="904" height="433" alt="03_1 2" src="https://github.com/user-attachments/assets/d4d6f417-3cb8-478b-9e45-a9fffcc91f15" />

#### Pembahasan


```python
uv python pin 3.14
```

<img width="468" height="67" alt="04" src="https://github.com/user-attachments/assets/c4061f8a-48ba-4b90-8140-719bc8807fa1" />

#### Pembahasan


```python
type .python-version
python --version
```

<img width="469" height="56" alt="05" src="https://github.com/user-attachments/assets/178235a3-991d-46ea-a49c-d733a38b3ac2" />

#### Pembahasan


### 1.3 Buat dan aktifkan environment

```python
uv venv
.venv\Scripts\activate.bat
where python
```

<img width="735" height="240" alt="06_1 3" src="https://github.com/user-attachments/assets/cab6ab8d-6dfb-4b04-9387-6584e8a31361" />

#### Pembahasan

### 1.4 Install FastAPI dan SQLModel

Paket FastAPI dan SQLModel dipasang dengan perintah berikut.

```python
uv pip install "fastapi[standard]" sqlmodel
```

```python
Resolved 61 packages in 2.95s
Prepared 6 packages in 2.14s
░░░░░░░░░░░░░░░░░░░░ [0/61] Installing wheels...                     warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 61 packages in 5.61s
 + agent-detector==2.0.0
 + annotated-doc==0.0.7
 + annotated-types==0.8.0
 + anyio==4.16.0
 + certifi==2026.11.20
 + charset-normalizer==3.5.3
 + click==8.5.1
 + colorama==0.4.6
 + detect-installer==0.2.1
 + dnspython==2.9.2
 + email-validator==2.4.0
 + fastapi==0.165.0
 + fastapi-cli==0.0.34
 + fastapi-cloud-cli==0.28.0
 + fastar==0.12.0
 + googleapis-common-protos==1.76.0
 + h11==0.16.0
 + httpcore==1.0.9
 + httpcore2==2.16.2
 + httptools==0.9.0
 + httpx==0.28.1
 + httpx2==2.16.2
 + idna==3.20
 + jinja2==3.1.6
 + markdown-it-py==4.3.0
 + markupsafe==3.0.4
 + mdurl==0.1.2
 + opentelemetry-api==1.45.2
 + opentelemetry-exporter-http-transport==0.66b2
 + opentelemetry-exporter-otlp-common==0.66b2
 + opentelemetry-exporter-otlp-proto-common==1.45.2
 + opentelemetry-exporter-otlp-proto-http==1.45.2
 + opentelemetry-proto==1.45.2
 + opentelemetry-sdk==1.45.2
 + opentelemetry-semantic-conventions==0.66b2
 + protobuf==7.36.2
 + pydantic==2.14.4
 + pydantic-core==2.50.5
 + pydantic-extra-types==2.11.1
 + pydantic-settings==2.16.3
 + pygments==2.21.0
 + python-dotenv==1.2.4
 + python-multipart==0.0.34
 + pyyaml==6.0.4
 + requests==2.34.2
 + rich==15.0.0
 + rich-toolkit==0.20.6
 + rignore==0.8.1
 + sentry-sdk==3.0.1
 + shellingham==1.5.4
 + sqlalchemy==2.1.9
 + sqlmodel==0.0.50
 + starlette==1.10.0
 + truststore==0.10.5
 + typer==0.29.2
 + typing-extensions==4.16.0
 + typing-inspection==0.4.5
 + urllib3==2.8.0
 + uvicorn==0.54.0
 + watchfiles==1.3.0
 + websockets==17.4
```

#### Pembahasan


<p align="justify">Proses instalasi Python dilakukan menggunakan uv dengan versi 3.14.4. Sebelum memulai instalasi, terlebih dahulu dilakukan pengecekan terhadap daftar versi Python yang tersedia dan dikenali oleh uv melalui perintah berikut.</p>

```python
uv pip list
```

```python
Package                                  Version
---------------------------------------- ----------
agent-detector                           2.0.0
annotated-doc                            0.0.7
annotated-types                          0.8.0
anyio                                    4.16.0
certifi                                  2026.11.20
charset-normalizer                       3.5.3
click                                    8.5.1
colorama                                 0.4.6
detect-installer                         0.2.1
dnspython                                2.9.2
email-validator                          2.4.0
fastapi                                  0.165.0
fastapi-cli                              0.0.34
fastapi-cloud-cli                        0.28.0
fastar                                   0.12.0
googleapis-common-protos                 1.76.0
h11                                      0.16.0
httpcore                                 1.0.9
httpcore2                                2.16.2
httptools                                0.9.0
httpx                                    0.28.1
httpx2                                   2.16.2
idna                                     3.20
jinja2                                   3.1.6
markdown-it-py                           4.3.0
markupsafe                               3.0.4
mdurl                                    0.1.2
opentelemetry-api                        1.45.2
opentelemetry-exporter-http-transport    0.66b2
opentelemetry-exporter-otlp-common       0.66b2
opentelemetry-exporter-otlp-proto-common 1.45.2
opentelemetry-exporter-otlp-proto-http   1.45.2
opentelemetry-proto                      1.45.2
opentelemetry-sdk                        1.45.2
opentelemetry-semantic-conventions       0.66b2
protobuf                                 7.36.2
pydantic                                 2.14.4
pydantic-core                            2.50.5
pydantic-extra-types                     2.11.1
pydantic-settings                        2.16.3
pygments                                 2.21.0
python-dotenv                            1.2.4
python-multipart                         0.0.34
pyyaml                                   6.0.4
requests                                 2.34.2
rich                                     15.0.0
rich-toolkit                             0.20.6
rignore                                  0.8.1
sentry-sdk                               3.0.1
shellingham                              1.5.4
sqlalchemy                               2.1.9
sqlmodel                                 0.0.50
starlette                                1.10.0
truststore                               0.10.5
typer                                    0.29.2
typing-extensions                        4.16.0
typing-inspection                        0.4.5
urllib3                                  2.8.0
uvicorn                                  0.54.0
watchfiles                               1.3.0
websockets                               17.4
```

#### Pembahasan


```python
uv pip freeze > requirements.txt
type requirements.txt
```

```python
agent-detector==2.0.0
annotated-doc==0.0.7
annotated-types==0.8.0
anyio==4.16.0
certifi==2026.11.20
charset-normalizer==3.5.3
click==8.5.1
colorama==0.4.6
detect-installer==0.2.1
dnspython==2.9.2
email-validator==2.4.0
fastapi==0.165.0
fastapi-cli==0.0.34
fastapi-cloud-cli==0.28.0
fastar==0.12.0
googleapis-common-protos==1.76.0
h11==0.16.0
httpcore==1.0.9
httpcore2==2.16.2
httptools==0.9.0
httpx==0.28.1
httpx2==2.16.2
idna==3.20
jinja2==3.1.6
markdown-it-py==4.3.0
markupsafe==3.0.4
mdurl==0.1.2
opentelemetry-api==1.45.2
opentelemetry-exporter-http-transport==0.66b2
opentelemetry-exporter-otlp-common==0.66b2
opentelemetry-exporter-otlp-proto-common==1.45.2
opentelemetry-exporter-otlp-proto-http==1.45.2
opentelemetry-proto==1.45.2
opentelemetry-sdk==1.45.2
opentelemetry-semantic-conventions==0.66b2
protobuf==7.36.2
pydantic==2.14.4
pydantic-core==2.50.5
pydantic-extra-types==2.11.1
pydantic-settings==2.16.3
pygments==2.21.0
python-dotenv==1.2.4
python-multipart==0.0.34
pyyaml==6.0.4
requests==2.34.2
rich==15.0.0
rich-toolkit==0.20.6
rignore==0.8.1
sentry-sdk==3.0.1
shellingham==1.5.4
sqlalchemy==2.1.9
sqlmodel==0.0.50
starlette==1.10.0
truststore==0.10.5
typer==0.29.2
typing-extensions==4.16.0
typing-inspection==0.4.5
urllib3==2.8.0
uvicorn==0.54.0
watchfiles==1.3.0
websockets==17.4
```

### 1.5 Install SQLite (command-line tools)

<img width="947" height="425" alt="07_1 5" src="https://github.com/user-attachments/assets/b79ab030-41af-448c-86fc-81d548f49705" />

Cari lokasi sqlite3.exe untuk memastikan:
```python
where /r . sqlite3.exe
```

Daftarkan ke PATH
```python
set "PATH=%PATH%;%CD%\sqlite-tools-win-x64-3540100"
sqlite3 --version
```

<img width="466" height="89" alt="08" src="https://github.com/user-attachments/assets/5b576e24-898d-41b9-a61a-bce166dd6ae1" />

#### Pembahasan



# TUGAS

### Buat satu tabel baru menggunakan SQLite, tabel berbeda dari yang ada pada contoh. Tabel tersebut mempunyai 1 primary key dan setidaknya berisi data dengan tipe INT, CHAR, VARCHAR, BOOLEAN, dan FLOAT.

###
###



---

#  PEMBAHASAN/PRASYARAT

---
# KESIMPULAN


---

# REFERENSI




