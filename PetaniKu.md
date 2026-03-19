# 🌾 PetaniKu - Aplikasi Pencatat Kegiatan Pertanian

## 📋 Deskripsi Proyek
**PetaniKu** adalah aplikasi web berbasis Flask yang dirancang khusus untuk membantu petani melacak kegiatan pertanian mereka dengan mudah dan terstruktur.

### Fitur Utama:
1. **Dashboard** - Ringkasan aktivitas harian dan statistik penting
2. **Pencatatan Kegiatan** - Catat pupuk, siram, panen, dan pestisida
3. **Riwayat Lengkap** - Lihat semua catatan dengan filter dan pencarian
4. **Jadwal Kegiatan** - Kelola dan pantau jadwal perawatan
5. **Eksperimen Pupuk** - Lacak eksperimen pupuk 3 dan 6 bulan

---

## 🚀 Instalasi & Setup

### Prasyarat:
- Python 3.8+
- pip (Python package manager)

### Langkah Instalasi:

#### 1. Clone Repository
```bash
git clone https://github.com/pinnedbyme/Farmtastic.git
cd Farmtastic/petaniku
```

#### 2. Buat Virtual Environment

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

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Jalankan Aplikasi
```bash
python run.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

---

## 📁 Struktur Direktori

```
petaniku/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # SQLAlchemy models (Tanaman, LogKegiatan, Jadwal, Eksperimen)
│   ├── routes.py            # Flask routes & API endpoints
│   └── templates/           # HTML templates
│       ├── base.html        # Base template dengan CSS global
│       ├── dashboard.html   # Halaman utama
│       ├── catat.html       # Form pencatatan kegiatan
│       ├── jadwal.html      # Kelola jadwal
│       ├── riwayat.html     # Riwayat kegiatan dengan filter
│       └── eksperimen.html  # Tracking eksperimen pupuk
├── instance/
│   └── database.db          # SQLite database (auto-created)
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── README.md               # Dokumentasi ini
```

---

## 🗄️ Database Schema

### Tanaman
| Kolom | Tipe | Deskripsi |
|-------|------|----------|
| id | Integer | Primary key |
| nama | String(100) | Nama tanaman (unik) |
| jenis | String(100) | Jenis tanaman (cth: Mangga, Cabai) |
| lokasi | String(255) | Lokasi penanaman |
| created_at | DateTime | Waktu pembuatan |

### LogKegiatan
| Kolom | Tipe | Deskripsi |
|-------|------|----------|
| id | Integer | Primary key |
| tanggal | Date | Tanggal kegiatan |
| tanaman_id | Integer | Foreign key ke Tanaman |
| jenis | String(50) | Jenis: pupuk/siram/panen/pestisida |
| detail | String(200) | Detail kegiatan |
| dosis | String(100) | Dosis/jumlah |
| catatan | Text | Catatan tambahan |
| created_at | DateTime | Waktu pencatatan |

### Jadwal
| Kolom | Tipe | Deskripsi |
|-------|------|----------|
| id | Integer | Primary key |
| tanggal | Date | Tanggal jadwal |
| jam | String(5) | Format HH:MM |
| kegiatan | String(200) | Deskripsi kegiatan |
| sudah_dilakukan | Boolean | Status penyelesaian |
| created_at | DateTime | Waktu pembuatan |

### Eksperimen
| Kolom | Tipe | Deskripsi |
|-------|------|----------|
| id | Integer | Primary key |
| tanaman_id | Integer | Foreign key ke Tanaman |
| tanggal_mulai | Date | Tanggal mulai eksperimen |
| pupuk_digunakan | String(200) | Nama/tipe pupuk |
| dosis | String(100) | Dosis pupuk |
| target_3bln | Text | Target 3 bulan |
| target_6bln | Text | Target 6 bulan |
| hasil_3bln | Text | Hasil observasi 3 bulan |
| hasil_6bln | Text | Hasil observasi 6 bulan |
| status | String(50) | aktif/selesai/dibatalkan |
| created_at | DateTime | Waktu pembuatan |

---

## 🔌 API Endpoints

### Dashboard
- `GET /` - Halaman utama dengan ringkasan

### Tanaman Management
- `GET /tanaman` - Daftar tanaman
- `POST /tanaman` - Tambah tanaman baru
- `POST /tanaman/<id>/hapus` - Hapus tanaman

### Catatan Kegiatan
- `GET /catat` - Form pencatatan
- `POST /catat` - Simpan catatan baru
- `GET /riwayat` - Lihat riwayat (support filter & search)
- `POST /api/log/<id>/delete` - Hapus catatan

### Jadwal
- `GET /jadwal` - Daftar jadwal
- `POST /jadwal` - Buat jadwal baru
- `POST /api/jadwal/<id>/selesai` - Toggle status jadwal
- `POST /api/jadwal/<id>/delete` - Hapus jadwal

### Eksperimen Pupuk
- `GET /eksperimen` - Daftar eksperimen
- `POST /eksperimen` - Mulai eksperimen baru
- `POST /eksperimen/<id>/update` - Update hasil/status eksperimen

---

## 🎨 Desain & UI/UX

### Teknologi:
- **Frontend**: HTML5, Tailwind CSS, Alpine.js
- **Backend**: Flask 2.3.3, SQLAlchemy 3.0.5
- **Database**: SQLite (mudah di-migrate ke PostgreSQL)
- **Font**: Google Fonts (Poppins + Plus Jakarta Sans)

### Design Features:
- ✅ Mobile-first responsive design
- ✅ Gradient backgrounds dan smooth animations
- ✅ Bottom navigation bar (farmer-friendly)
- ✅ Emoji icons untuk visual clarity
- ✅ High contrast colors (Teal #0f766e + Amber #f59e0b)
- ✅ Large touch targets (accessibility)

---

## 🔧 Troubleshooting

### Error: `venv/bin/activate: No such file or directory`
**Solusi**: Buat virtual environment baru
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# atau
venv\Scripts\activate     # Windows
```

### Error: `ModuleNotFoundError: No module named 'flask'`
**Solusi**: Install dependencies
```bash
pip install -r requirements.txt
```

### Database Errors
**Solusi**: Hapus `instance/database.db` dan jalankan lagi (database akan otomatis dibuat)
```bash
rm instance/database.db
python run.py
```

### Port 5000 Sudah Digunakan
**Solusi**: Edit `run.py` dan ubah port, atau kill proses:
```bash
# Linux/Mac
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

---

## 📝 Catatan Pengembang

- **Database**: Menggunakan SQLite dengan SQLAlchemy ORM
- **Cascading Delete**: Menghapus tanaman akan otomatis menghapus semua LogKegiatan terkait
- **Development Mode**: Debug=True untuk auto-reload saat development
- **Future**: Dapat dengan mudah di-migrate ke PostgreSQL dengan mengubah connection string

---

## 📞 Support

Jika ada pertanyaan atau bug report, silakan buat issue di GitHub repository.

---

**Happy Farming! 🌾**
