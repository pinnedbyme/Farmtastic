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
                         tanaman_list=tanaman_list,
                         today=today)

# ==================== CATAT KEGIATAN ====================
@main_bp.route('/catat', methods=['GET', 'POST'])
def catat_kegiatan():
    if request.method == 'POST':
        tanggal = request.form.get('tanggal')
        tanaman_nama = request.form.get('tanaman_nama')
        tanaman_id = request.form.get('tanaman_id')
        jenis = request.form.get('jenis')
        detail = request.form.get('detail', '')
        dosis = request.form.get('dosis', '')
        catatan = request.form.get('catatan', '')
        
        # Jika tanaman baru, buat entri baru
        if not tanaman_id and tanaman_nama:
            jenis_tanaman = request.form.get('jenis_tanaman', 'Tanaman')
            lokasi = request.form.get('lokasi', '')
            tanaman = Tanaman(nama=tanaman_nama, jenis=jenis_tanaman, lokasi=lokasi)
            db.session.add(tanaman)
            db.session.flush()
            tanaman_id = tanaman.id
        
        log = LogKegiatan(
            tanggal=datetime.strptime(tanggal, '%Y-%m-%d').date(),
            tanaman_id=int(tanaman_id),
            jenis=jenis,
            detail=detail,
            dosis=dosis,
            catatan=catatan
        )
        db.session.add(log)
        db.session.commit()
        
        return redirect(url_for('main.dashboard'))
    
    tanaman_list = Tanaman.query.all()
    return render_template('catat.html', tanaman_list=tanaman_list, today=datetime.utcnow().date())

# ==================== JADWAL KERJA ====================
@main_bp.route('/jadwal', methods=['GET', 'POST'])
def jadwal():
    if request.method == 'POST':
        tanggal = request.form.get('tanggal')
        jam = request.form.get('jam')
        kegiatan = request.form.get('kegiatan')
        
        jadwal_baru = Jadwal(
            tanggal=datetime.strptime(tanggal, '%Y-%m-%d').date(),
            jam=jam,
            kegiatan=kegiatan
        )
        db.session.add(jadwal_baru)
        db.session.commit()
        
        return redirect(url_for('main.jadwal'))
    
    today = datetime.utcnow().date()
    jadwal_list = Jadwal.query.filter(Jadwal.tanggal >= today).order_by(Jadwal.tanggal, Jadwal.jam).all()
    
    return render_template('jadwal.html', jadwal_list=jadwal_list, today=today)

# ==================== RIWAYAT ====================
@main_bp.route('/riwayat')
def riwayat():
    filter_jenis = request.args.get('filter', 'semua')
    search = request.args.get('search', '')
    
    query = LogKegiatan.query
    
    if filter_jenis != 'semua':
        query = query.filter_by(jenis=filter_jenis)
    
    if search:
        query = query.join(Tanaman).filter(
            db.or_(
                Tanaman.nama.ilike(f'%{search}%'),
                LogKegiatan.detail.ilike(f'%{search}%'),
                LogKegiatan.catatan.ilike(f'%{search}%')
            )
        )
    
    log_list = query.order_by(LogKegiatan.tanggal.desc()).all()
    
    return render_template('riwayat.html', log_list=log_list, filter_jenis=filter_jenis, search=search)

# ==================== EKSPERIMEN ====================
@main_bp.route('/eksperimen', methods=['GET', 'POST'])
def eksperimen():
    if request.method == 'POST':
        tanaman_id = request.form.get('tanaman_id')
        pupuk_digunakan = request.form.get('pupuk_digunakan')
        dosis = request.form.get('dosis', '')
        target_3bln = request.form.get('target_3bln', '')
        target_6bln = request.form.get('target_6bln', '')
        
        exp = Eksperimen(
            tanaman_id=int(tanaman_id),
            pupuk_digunakan=pupuk_digunakan,
            dosis=dosis,
            target_3bln=target_3bln,
            target_6bln=target_6bln,
            status='aktif'
        )
        db.session.add(exp)
        db.session.commit()
        
        return redirect(url_for('main.eksperimen'))
    
    eksperimen_list = Eksperimen.query.all()
    tanaman_list = Tanaman.query.all()
    
    return render_template('eksperimen.html', eksperimen_list=eksperimen_list, tanaman_list=tanaman_list)

# ==================== API - Mark Jadwal Done ====================
@main_bp.route('/api/jadwal/<int:jadwal_id>/done', methods=['POST'])
def mark_jadwal_done(jadwal_id):
    jadwal = Jadwal.query.get_or_404(jadwal_id)
    jadwal.sudah_dilakukan = not jadwal.sudah_dilakukan
    db.session.commit()
    return jsonify({'success': True, 'sudah_dilakukan': jadwal.sudah_dilakukan})

# ==================== API - Delete ====================
@main_bp.route('/api/log/<int:log_id>/delete', methods=['POST'])
def delete_log(log_id):
    log = LogKegiatan.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    return jsonify({'success': True})

@main_bp.route('/api/jadwal/<int:jadwal_id>/delete', methods=['POST'])
def delete_jadwal(jadwal_id):
    jadwal = Jadwal.query.get_or_404(jadwal_id)
    db.session.delete(jadwal)
    db.session.commit()
    return jsonify({'success': True})

@main_bp.route('/api/eksperimen/<int:exp_id>/delete', methods=['POST'])
def delete_eksperimen(exp_id):
    exp = Eksperimen.query.get_or_404(exp_id)
    db.session.delete(exp)
    db.session.commit()
    return jsonify({'success': True})
