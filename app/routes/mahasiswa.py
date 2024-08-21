from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from app.models import *

mahasiswa_bp = Blueprint('mahasiswa', __name__)

@mahasiswa_bp.route('/mahasiswa/dashboard')
@login_required
def dashboard():
    if current_user.peran != 'mahasiswa':
        flash(f'Anda tidak memiliki akses ke halaman {url_for(request.endpoint)}.', 'error')
        return redirect(url_for(f'{current_user.peran}.dashboard'))
    
    return render_template('mahasiswa/dashboard.html')

@mahasiswa_bp.route('/mahasiswa/daftar_matakuliah')
@login_required
def daftar_matakuliah():
    if current_user.peran != 'mahasiswa':
        flash(f'Anda tidak memiliki akses ke halaman {url_for(request.endpoint)}.', 'error')
        return redirect(url_for(f'{current_user.peran}.dashboard'))
    
    mahasiswa = Mahasiswa.query.filter_by(pengguna_id=current_user.id).first()
    
    pendaftarans = Pendaftaran.query.filter_by(mahasiswa_id=mahasiswa.id).all()
    
    # Mengambil mata kuliah yang terdaftar
    mata_kuliah_list = []
    for pendaftaran in pendaftarans:
        mata_kuliah = MataKuliah.query.get(pendaftaran.mata_kuliah_id)
        mata_kuliah_list.append(mata_kuliah)
    
    return render_template('mahasiswa/daftar_matakuliah.html', daftar_matkul=mata_kuliah_list)

@mahasiswa_bp.route('/mahasiswa/daftar_nilai')
@login_required
def daftar_nilai():
    if current_user.peran != 'mahasiswa':
        flash(f'Anda tidak memiliki akses ke halaman {url_for(request.endpoint)}.', 'error')
        return redirect(url_for(f'{current_user.peran}.dashboard'))
    
    mahasiswa = Mahasiswa.query.filter_by(pengguna_id=current_user.id).first()
    
    pendaftarans = Pendaftaran.query.filter_by(mahasiswa_id=mahasiswa.id).all()
    
    return render_template('mahasiswa/daftar_nilai.html', pendaftaran_list=pendaftarans)