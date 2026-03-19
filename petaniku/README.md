# 🌾 PetaniKu - Aplikasi Catatan Pertanian

Aplikasi web modern untuk petani mencatat dan melacak kegiatan pertanian, jadwal kerja, dan eksperimen pupuk.

## ✨ Fitur Utama

- 📊 **Dashboard** - Overview kegiatan hari ini, jadwal besok, dan eksperimen aktif
- ✍️ **Catat Kegiatan** - Log aktivitas (siram, pupuk, pestisida, panen) dengan mudah
- 📅 **Jadwal Kerja** - Rencanakan kegiatan dengan sistem penjadwalan
- 📜 **Riwayat Lengkap** - Lihat history kegiatan dengan fitur search dan filter
- 🔬 **Eksperimen Pupuk** - Track penggunaan pupuk dan pantau hasil setelah 3-6 bulan

## 🛠️ Tech Stack

- **Backend**: Python Flask + SQLAlchemy ORM
- **Database**: SQLite (production-ready)
- **Frontend**: HTML5 + Tailwind CSS + Alpine.js
- **Fonts**: Google Fonts (Poppins, Plus Jakarta Sans)
- **Design**: Mobile-first responsive design

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)
- Git (untuk clone)

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/pinnedbyme/Farmtastic.git
cd Farmtastic/petaniku
```

### 2. Buat Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Ini akan install:
- Flask==2.3.3
- Flask-SQLAlchemy==3.0.5
- python-dateutil==2.8.2
- Werkzeug==2.3.7

### 4. Jalankan Aplikasi

```bash
python run.py
```

Anda akan melihat output:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 5. Buka di Browser

Kunjungi: **http://localhost:5000**

## 📁 Struktur Folder

```
petaniku/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models (SQLAlchemy)
│   ├── routes.py                # API routes dan endpoints
│   ├── templates/               # HTML templates
│   │   ├── base.html            # Base layout
│   │   ├── dashboard.html       # Halaman utama
│   │   ├── catat.html           # Form catat kegiatan
│   │   ├── jadwal.html          # Jadwal kerja
│   │   ├── riwayat.html         # History view
│   │   └── eksperimen.html      # Eksperimen pupuk
│   └── static/                  # CSS & JavaScript
├── instance/
│   └── database.db              # SQLite database
├── run.py                       # Entry point
├── requirements.txt             # Python dependencies
└── README.md                    # File ini
```

## 🎯 Cara Menggunakan

### Dashboard
- Lihat overview kegiatan hari ini
- Cek jadwal untuk besok
- Monitor eksperimen pupuk yang sedang berjalan
- Lihat pupuk yang diberikan minggu ini

### Catat Kegiatan
1. Pilih tanaman yang akan dicatat
2. Pilih jenis kegiatan (siram, pupuk, pestisida, panen)
3. Isi detail dan dosis
4. Tambahkan catatan (opsional)
5. Klik "Simpan Kegiatan"

### Jadwal Kerja
1. Buka halaman Jadwal
2. Isi tanggal dan jam
3. Deskripsi kegiatan apa yang ingin dilakukan
4. Klik "Simpan Jadwal"
5. Jadwal akan muncul di Dashboard

### Riwayat
- Gunakan filter untuk melihat jenis kegiatan tertentu
- Gunakan search untuk mencari catatan spesifik
- Lihat detail lengkap setiap kegiatan

### Eksperimen
1. Pilih tanaman untuk dieksperi
2. Isi data pupuk yang digunakan
3. Set target 3 bulan dan 6 bulan
4. Sistem akan otomatis memberi reminder setelah periode waktu

## 🎨 Design Features

- **Modern Typography**: Google Fonts (Poppins + Plus Jakarta Sans)
- **Color Palette**: Teal (#0f766e) + Amber (#f59e0b)
- **Responsive**: Mobile-first design bekerja sempurna di HP dan tablet
- **Smooth Animations**: Gradient backgrounds dan smooth transitions
- **Accessibility**: High contrast colors, large fonts (18px+)

## 📱 Mobile Compatibility

Aplikasi fully responsive dan dioptimalkan untuk:
- ✓ Smartphone
- ✓ Tablet
- ✓ Desktop/Laptop

Bottom navigation memudahkan navigasi di mobile devices.

## 🔧 Konfigurasi

### Mengubah Port

Edit `run.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Ubah 5000 ke 8000
```

### Database

Database SQLite otomatis dibuat di: `instance/database.db`

Jika ingin reset database, hapus file tersebut lalu jalankan aplikasi lagi.

## 🆘 Troubleshooting

### "python: command not found"
- Install Python dari https://www.python.org/downloads/
- Pastikan checklist "Add Python to PATH" saat install

### "ModuleNotFoundError: No module named 'flask'"
- Pastikan virtual environment sudah aktivasi
- Jalankan `pip install -r requirements.txt` lagi

### "Address already in use" port 5000
- Port 5000 sudah dipakai aplikasi lain
- Ubah port di `run.py` atau close aplikasi yang menggunakan port 5000

### Database corruption
- Hapus `instance/database.db`
- Jalankan `python run.py` lagi (database akan recreate)

## 📝 API Endpoints

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| GET | `/` | Dashboard |
| GET/POST | `/catat` | Halaman catat kegiatan |
| GET/POST | `/jadwal` | Halaman jadwal |
| GET | `/riwayat` | Halaman riwayat |
| GET/POST | `/eksperimen` | Halaman eksperimen |
| POST | `/api/jadwal/<id>/done` | Mark jadwal selesai |
| POST | `/api/log/<id>/delete` | Hapus log kegiatan |
| POST | `/api/jadwal/<id>/delete` | Hapus jadwal |
| POST | `/api/eksperimen/<id>/delete` | Hapus eksperimen |

## 🚀 Deployment

### Development
```bash
python run.py
```

### Production
Gunakan WSGI server seperti Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## 📚 Dokumentasi Lengkap

Lihat file `BETA_RELEASE.md` di root repository untuk dokumentasi lengkap.

## 👨‍💻 Developer Notes

- **Debug Mode**: ON (otomatis reload saat ada perubahan file)
- **Database**: SQLite dengan SQLAlchemy ORM
- **Frontend**: Tailwind CSS dengan Alpine.js untuk interaksi
- **Konvensi Kode**: PEP 8 untuk Python, BEM untuk CSS

## 📄 Lisensi

Bebas digunakan untuk keperluan pribadi dan komersial.

## 📞 Support

Jika ada pertanyaan atau issue:
1. Lihat troubleshooting section di atas
2. Check GitHub Issues: https://github.com/pinnedbyme/Farmtastic/issues
3. Baca BETA_RELEASE.md untuk info lebih

---

**Happy Farming! 🌾**

Dibuat dengan ❤️ untuk petani Indonesia
