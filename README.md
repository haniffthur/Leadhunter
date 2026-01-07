# 🕵️‍♂️ Hunter System - AI Lead Generation

**Hunter System** adalah aplikasi CRM pintar untuk mencari klien bisnis (Leads) secara otomatis menggunakan AI.
Aplikasi ini menggabungkan **Google Maps (via Serper)** untuk mencari data, dan **Google Gemini AI** untuk menganalisa bisnis tersebut.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)

## 🔥 Fitur Utama
1.  **🤖 Robot Hunter:** Cari data bisnis (Nama, Alamat, No HP) otomatis.
2.  **🧠 AI Analyst:** Gemini AI menebak kategori bisnis & teknologi website calon klien.
3.  **📄 Proposal PDF:** Download surat penawaran resmi dalam 1 klik.
4.  **💬 WhatsApp Blast:** Tombol chat WA otomatis dengan template pesan personal.
5.  **📊 Dashboard:** Visualisasi data leads dan potensi omzet.

---

## 🛠️ Cara Install (Setup Guide)

Ikuti langkah-langkah ini di terminal (Command Prompt / PowerShell / Terminal VS Code).

2. Bikin Virtual Environment (Wajib)
Biar library tidak bentrok, kita bikin ruang isolasi dulu.

Untuk Windows:

Bash

python -m venv env
env\Scripts\activate
Untuk Mac / Linux:

Bash

python3 -m venv env
source env/bin/activate
(Tanda berhasil: Ada tulisan (env) di sebelah kiri terminal kamu)


3. Install Library
Install semua "bumbu" yang dibutuhkan aplikasi ini.

Bash

pip install -r requirements.txt


4. Setting API Key (PENTING ⚠️)
Aplikasi ini butuh "bensin" berupa API Key gratisan agar Robot bisa jalan.

Daftar di serper.dev (Untuk Search Google). Copy API Key.

Daftar di aistudio.google.com (Untuk Otak AI). Copy API Key.

Buka file di folder project: dashboard/utils.py.

Paste key kamu di bagian atas file:

Python

SERPER_API_KEY = "PASTE_KEY_SERPER_DISINI"
GEMINI_API_KEY = "PASTE_KEY_GEMINI_DISINI"


5. Setup Database
Siapkan database dan bikin akun admin untuk login.

Bash

python manage.py migrate
python manage.py createsuperuser

6. Jalankan Server 🚀
Nyalakan mesin aplikasi.

Bash

python manage.py runserver


7. Login
Buka browser (Chrome/Edge) dan akses alamat ini: 👉 https://www.google.com/search?q=http://127.0.0.1:8000/admin/

Login pakai username & password yang kamu buat di langkah no 5