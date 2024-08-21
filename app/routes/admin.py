from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from app.models import Pengguna
from ..utils import peran_required
from ..models import *

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():

    if current_user.peran != 'admin':
        flash(f'Anda tidak memiliki akses ke halaman {url_for(request.endpoint)}.', 'error')
        return redirect(url_for(f'{current_user.peran}.dashboard'))
    
    return render_template('admin/dashboard.html')

@admin_bp.route('/manage_users')
@login_required
def manage_users():
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))
    pengguna_list = Pengguna.query.all()
    return render_template('admin/manage_users.html', pengguna=pengguna_list)

@admin_bp.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        role = request.form['peran']
        nama_pengguna = request.form['nama_pengguna']
        email = request.form['email']
        kata_sandi = request.form['kata_sandi']
        
        # Cek apakah username sudah ada
        existing_user = Pengguna.query.filter_by(nama_pengguna=nama_pengguna).first()
        if existing_user:
            flash('Username sudah ada, silakan pilih yang lain.', 'error')
            return redirect(url_for('admin.add_user'))

        # Cek apakah email sudah ada
        existing_email = Pengguna.query.filter_by(email=email).first()
        if existing_email:
            flash('Email sudah terdaftar, silakan gunakan email lain.', 'error')
            return redirect(url_for('admin.add_user'))

        # Tambahkan pengguna baru
        new_user = Pengguna(nama_pengguna=nama_pengguna, email=email, kata_sandi=kata_sandi, peran=role)

        if role == 'dosen':
            nik = request.form['nik']
            # Cek apakah NIK sudah ada
            existing_nik = Dosen.query.filter_by(nik=nik).first()
            if existing_nik:
                flash('NIK sudah terdaftar, silakan gunakan NIK lain.', 'error')
                return redirect(url_for('admin.add_user'))

            nama = request.form['nama']
            tanggal_lahir = request.form['tanggal_lahir']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']
            nomor_telepon = request.form['nomor_telepon']
            spesialisasi = request.form['spesialisasi']
            
            new_user.peran = 'dosen'
            new_dosen = Dosen(nik=nik, nama=nama, tanggal_lahir=tanggal_lahir,
                              jenis_kelamin=jenis_kelamin, alamat=alamat,
                              nomor_telepon=nomor_telepon, pengguna=new_user, spesialisasi=spesialisasi)
            db.session.add(new_dosen)

        elif role == 'mahasiswa':
            nim = request.form['nim']
            # Cek apakah NIM sudah ada
            existing_nim = Mahasiswa.query.filter_by(nim=nim).first()
            if existing_nim:
                flash('NIM sudah terdaftar, silakan gunakan NIM lain.', 'error')
                return redirect(url_for('admin.add_user'))

            nama = request.form['nama']
            tanggal_lahir = request.form['tanggal_lahir']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']
            nomor_telepon = request.form['nomor_telepon']
            tahun_masuk = request.form['tahun_masuk']
            
            new_user.peran = 'mahasiswa'
            new_mahasiswa = Mahasiswa(nim=nim, nama=nama, tanggal_lahir=tanggal_lahir,
                                      jenis_kelamin=jenis_kelamin, alamat=alamat,
                                      nomor_telepon=nomor_telepon, tahun_masuk=tahun_masuk,
                                      pengguna=new_user)
            db.session.add(new_mahasiswa)

        db.session.add(new_user)
        db.session.commit()
        flash('Akun berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.manage_users'))
    
    # get request parameter
    role = request.args.get('role')

    if role == 'dosen':
        return render_template('admin/tambah_dosen.html')
    elif role == 'mahasiswa':
        return render_template('admin/tambah_mahasiswa.html')
    elif role == 'admin':
        return render_template('admin/tambah_admin.html')

    return redirect(url_for('admin.dashboard'))
