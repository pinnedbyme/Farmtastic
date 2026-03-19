from . import db
from datetime import datetime

class Tanaman(db.Model):
    __tablename__ = 'tanaman'
    
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False, unique=True)
    jenis = db.Column(db.String(100), nullable=False)
    lokasi = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    log_kegiatan = db.relationship('LogKegiatan', backref='tanaman', lazy=True, cascade='all, delete-orphan')
    eksperimen = db.relationship('Eksperimen', backref='tanaman', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Tanaman {self.nama}>'


class LogKegiatan(db.Model):
    __tablename__ = 'log_kegiatan'
    
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    tanaman_id = db.Column(db.Integer, db.ForeignKey('tanaman.id'), nullable=False)
    jenis = db.Column(db.String(50), nullable=False)  # 'pupuk', 'siram', 'panen', 'pestisida'
    detail = db.Column(db.String(200))
    dosis = db.Column(db.String(100))
    catatan = db.Column(db.Text)
    foto_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LogKegiatan {self.jenis} - {self.tanggal}>'


class Jadwal(db.Model):
    __tablename__ = 'jadwal'
    
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date, nullable=False)
    jam = db.Column(db.String(5))  # format HH:MM
    kegiatan = db.Column(db.String(200), nullable=False)
    sudah_dilakukan = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Jadwal {self.kegiatan} - {self.tanggal}>'


class Eksperimen(db.Model):
    __tablename__ = 'eksperimen'
    
    id = db.Column(db.Integer, primary_key=True)
    tanaman_id = db.Column(db.Integer, db.ForeignKey('tanaman.id'), nullable=False)
    tanggal_mulai = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    pupuk_digunakan = db.Column(db.String(200), nullable=False)
    dosis = db.Column(db.String(100))
    target_3bln = db.Column(db.Text)
    target_6bln = db.Column(db.Text)
    hasil_3bln = db.Column(db.Text)
    hasil_6bln = db.Column(db.Text)
    status = db.Column(db.String(50), default='aktif')  # 'aktif', 'selesai', 'dibatalkan'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Eksperimen {self.pupuk_digunakan}>'
