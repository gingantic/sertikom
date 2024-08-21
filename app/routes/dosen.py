from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from ..models import *
from ..utils import peran_required

dosen_bp = Blueprint('dosen', __name__)

@dosen_bp.route('/dosen/dashboard')
@login_required
def dashboard():
    if current_user.peran != 'dosen':
        flash(f'Anda tidak memiliki akses ke halaman {url_for(request.endpoint)}.', 'error')
        return redirect(url_for(f'{current_user.peran}.dashboard'))
    
    return render_template('dosen/dashboard.html')

@dosen_bp.route('/dosen/daftar_matakuliah')
@login_required
def daftar_matakuliah():
    if current_user.peran != 'dosen':
        flash(f'Anda tidak memiliki akses ke halaman {url_for(request.endpoint)}.', 'error')
        return redirect(url_for(f'{current_user.peran}.dashboard'))
    
    dosen = Dosen.query.filter_by(pengguna_id=current_user.id).first()
    
    daftar_matkul = MataKuliah.query.filter_by(dosen_id=dosen.id).all()
    
    return render_template('dosen/daftar_matakuliah.html', daftar_matkul=daftar_matkul)

@dosen_bp.route('/dosen/manage_mahasiswa/<int:id>', methods=['GET', 'POST'])
@login_required
def manage_mahasiswa(id):
    if current_user.peran != 'dosen':
        flash(f'Anda tidak memiliki akses ke halaman {url_for(request.endpoint)}.', 'error')
        return redirect(url_for(f'{current_user.peran}.dashboard'))
    
    dosen = Dosen.query.filter_by(pengguna_id=current_user.id).first()
    
    daftar_matkul = MataKuliah.query.filter_by(id=id).first()

    if daftar_matkul.dosen_id != dosen.id:
        flash('Anda tidak memiliki akses ke Mata Kuliah ini.', 'error')
        return redirect(url_for('dosen.daftar_matakuliah'))
    
    daftar_mahasiswa = Pendaftaran.query.filter_by(mata_kuliah_id=id).all()

    return render_template('dosen/manage_mahasiswa.html', daftar_mahasiswa=daftar_mahasiswa)

@dosen_bp.route('/dosen/edit_nilai/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_nilai(id):
    if current_user.peran != 'dosen':
        flash(f'Anda tidak memiliki akses ke halaman {url_for(request.endpoint)}.', 'error')
        return redirect(url_for(f'{current_user.peran}.dashboard'))
    
    dosen = Dosen.query.filter_by(pengguna_id=current_user.id).first()

    pendaftaran = Pendaftaran.query.get(id)
    
    daftar_matkul = MataKuliah.query.filter_by(id=pendaftaran.mata_kuliah_id).first()

    if daftar_matkul.dosen_id != dosen.id:
        flash('Anda tidak memiliki akses ke Mata Kuliah ini.', 'error')
        return redirect(url_for('dosen.daftar_matakuliah'))
    
    if request.method == 'POST':
        status = request.form['status']
        nilai_akhir = request.form['nilai_akhir']

        # Validasi data
        if not status or not nilai_akhir:
            flash('Semua field harus diisi!', 'error')
            return redirect(url_for('dosen.daftar_matakuliah'))

        # Update data pendaftaran
        edit_nilai = Pendaftaran.query.get(id)
        edit_nilai.nilai_akhir = nilai_akhir
        edit_nilai.status = status

        db.session.commit()
        flash('Data Nilai berhasil diubah!', 'success')
        return redirect(url_for('dosen.manage_mahasiswa', id=pendaftaran.mata_kuliah_id))
    
    mahasiswa_list = Mahasiswa.query.all()
    matakuliah_list = MataKuliah.query.all()
    
    return render_template('dosen/edit_nilai.html', pendaftaran=pendaftaran, mahasiswa_list=mahasiswa_list, matakuliah_list=matakuliah_list)



# @dosen_bp.route('/detail')
# @login_required
# @peran_required('dosen')
# def detail():
#     dosen = Dosen.query.filter_by(pengguna_id=current_user.id).first()
#     return render_template('dosen/detail.html', dosen=dosen)
