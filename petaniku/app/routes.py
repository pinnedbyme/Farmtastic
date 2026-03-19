from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from . import db
from .models import Tanaman, LogKegiatan, Jadwal, Eksperimen
from datetime import datetime, timedelta
from sqlalchemy import func

main_bp = Blueprint('main', __name__)

# ==================== DASHBOARD ====================
@main_bp.route('/')
def dashboard():
    today = datetime.utcnow().date()
    
    # Ambil jadwal hari ini
    jadwal_hari_ini = Jadwal.query.filter_by(tanggal=today).all()
    
    # Ambil pupuk terakhir
    log_terakhir = LogKegiatan.query.filter_by(jenis='pupuk').order_by(LogKegiatan.tanggal.desc()).first()
    
    # Ambil jadwal besok
    besok = today + timedelta(days=1)
    jadwal_besok = Jadwal.query.filter_by(tanggal=besok).all()
    
    # Ambil eksperimen aktif
    eksperimen_aktif = Eksperimen.query.filter_by(status='aktif').all()
    
    # Hitung total kegiatan minggu ini
    seminggu_lalu = today - timedelta(days=7)
    pupuk_minggu_ini = LogKegiatan.query.filter(
        LogKegiatan.jenis == 'pupuk',
        LogKegiatan.tanggal >= seminggu_lalu,
        LogKegiatan.tanggal <= today
    ).count()
    
    tanaman_list = Tanaman.query.all()
    
    return render_template('dashboard.html', 
                         jadwal_hari_ini=jadwal_hari_ini,
                         log_terakhir=log_terakhir,
                         jadwal_besok=jadwal_besok,
                         eksperimen_aktif=eksperimen_aktif,
                         pupuk_minggu_ini=pupuk_minggu_ini,
                         tanaman_list=tanaman_list)

# ==================== TANAMAN ====================
@main_bp.route('/tanaman', methods=['GET', 'POST'])
def kelola_tanaman():
    if request.method == 'POST':
        nama = request.form.get('nama')
        jenis = request.form.get('jenis')
        lokasi = request.form.get('lokasi')
        
        tanaman = Tanaman(nama=nama, jenis=jenis, lokasi=lokasi)
        db.session.add(tanaman)
        db.session.commit()
        
        return redirect(url_for('main.kelola_tanaman'))
    
    tanaman_list = Tanaman.query.all()
    return render_template('tanaman.html', tanaman_list=tanaman_list)

@main_bp.route('/tanaman/<int:id>/hapus', methods=['POST'])
def hapus_tanaman(id):
    tanaman = Tanaman.query.get_or_404(id)
    db.session.delete(tanaman)
    db.session.commit()
    return jsonify({'success': True})

# ==================== CATAT KEGIATAN ====================
@main_bp.route('/catat', methods=['GET', 'POST'])
def catat_kegiatan():
    if request.method == 'POST':
        tanaman_id = request.form.get('tanaman_id')
        tanggal = request.form.get('tanggal')
        jenis = request.form.get('jenis')
        detail = request.form.get('detail')
        dosis = request.form.get('dosis')
        catatan = request.form.get('catatan')
        
        log = LogKegiatan(
            tanggal=datetime.strptime(tanggal, '%Y-%m-%d').date(),
            tanaman_id=tanaman_id,
            jenis=jenis,
            detail=detail,
            dosis=dosis,
            catatan=catatan
        )
        db.session.add(log)
        db.session.commit()
        
        return redirect(url_for('main.riwayat_kegiatan'))
    
    tanaman_list = Tanaman.query.all()
    return render_template('catat.html', tanaman_list=tanaman_list)

# ==================== RIWAYAT ====================
@main_bp.route('/riwayat')
def riwayat_kegiatan():
    search = request.args.get('search', '')
    filter_jenis = request.args.get('filter', 'semua')
    
    query = LogKegiatan.query
    
    if filter_jenis != 'semua':
        query = query.filter_by(jenis=filter_jenis)
    
    if search:
        query = query.join(Tanaman).filter(
            (Tanaman.nama.ilike(f'%{search}%')) |
            (LogKegiatan.detail.ilike(f'%{search}%')) |
            (LogKegiatan.dosis.ilike(f'%{search}%'))
        )
    
    log_list = query.order_by(LogKegiatan.tanggal.desc()).all()
    
    return render_template('riwayat.html', 
                         log_list=log_list,
                         search=search,
                         filter_jenis=filter_jenis)

@main_bp.route('/api/log/<int:id>/delete', methods=['POST'])
def delete_log(id):
    log = LogKegiatan.query.get_or_404(id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({'success': True})

# ==================== JADWAL ====================
@main_bp.route('/jadwal', methods=['GET', 'POST'])
def kelola_jadwal():
    if request.method == 'POST':
        tanggal = request.form.get('tanggal')
        jam = request.form.get('jam')
        kegiatan = request.form.get('kegiatan')
        
        jadwal = Jadwal(
            tanggal=datetime.strptime(tanggal, '%Y-%m-%d').date(),
            jam=jam,
            kegiatan=kegiatan
        )
        db.session.add(jadwal)
        db.session.commit()
        
        return redirect(url_for('main.kelola_jadwal'))
    
    jadwal_list = Jadwal.query.order_by(Jadwal.tanggal, Jadwal.jam).all()
    return render_template('jadwal.html', jadwal_list=jadwal_list)

@main_bp.route('/api/jadwal/<int:id>/selesai', methods=['POST'])
def selesai_jadwal(id):
    jadwal = Jadwal.query.get_or_404(id)
    jadwal.sudah_dilakukan = not jadwal.sudah_dilakukan
    db.session.commit()
    return jsonify({'success': True, 'status': jadwal.sudah_dilakukan})

@main_bp.route('/api/jadwal/<int:id>/delete', methods=['POST'])
def delete_jadwal(id):
    jadwal = Jadwal.query.get_or_404(id)
    db.session.delete(jadwal)
    db.session.commit()
    return jsonify({'success': True})

# ==================== EKSPERIMEN ====================
@main_bp.route('/eksperimen', methods=['GET', 'POST'])
def kelola_eksperimen():
    if request.method == 'POST':
        tanaman_id = request.form.get('tanaman_id')
        pupuk_digunakan = request.form.get('pupuk_digunakan')
        dosis = request.form.get('dosis')
        target_3bln = request.form.get('target_3bln')
        target_6bln = request.form.get('target_6bln')
        
        eksperimen = Eksperimen(
            tanaman_id=tanaman_id,
            pupuk_digunakan=pupuk_digunakan,
            dosis=dosis,
            target_3bln=target_3bln,
            target_6bln=target_6bln
        )
        db.session.add(eksperimen)
        db.session.commit()
        
        return redirect(url_for('main.kelola_eksperimen'))
    
    tanaman_list = Tanaman.query.all()
    eksperimen_list = Eksperimen.query.all()
    return render_template('eksperimen.html', 
                         tanaman_list=tanaman_list,
                         eksperimen_list=eksperimen_list)

@main_bp.route('/eksperimen/<int:id>/update', methods=['POST'])
def update_eksperimen(id):
    eksperimen = Eksperimen.query.get_or_404(id)
    
    if request.form.get('hasil_3bln'):
        eksperimen.hasil_3bln = request.form.get('hasil_3bln')
    if request.form.get('hasil_6bln'):
        eksperimen.hasil_6bln = request.form.get('hasil_6bln')
    if request.form.get('status'):
        eksperimen.status = request.form.get('status')
    
    db.session.commit()
    return redirect(url_for('main.kelola_eksperimen'))
