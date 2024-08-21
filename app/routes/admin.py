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

@admin_bp.route('/manage_mahasiswa')
@login_required
def manage_mahasiswa():
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))

    mahasiswa_list = Mahasiswa.query.all()
    return render_template('admin/manage_mahasiswa.html', mahasiswa_list=mahasiswa_list)

@admin_bp.route('/manage_dosen')
@login_required
def manage_dosen():
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))

    dosen_list = Dosen.query.all()
    return render_template('admin/manage_dosen.html', dosen_list=dosen_list)

@admin_bp.route('/manage_matakuliah')
@login_required
def manage_matakuliah():
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))

    matakuliah_list = MataKuliah.query.all()
    return render_template('admin/manage_matakuliah.html', matakuliah_list=matakuliah_list)

@admin_bp.route('/manage_pendaftaran')
@login_required
def manage_pendaftaran():
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))

    pendaftaran_list = Pendaftaran.query.all()
    return render_template('admin/manage_pendaftaranmatakuliah.html', pendaftaran_list=pendaftaran_list)

@admin_bp.route('/add_pendaftaran', methods=['GET', 'POST'])
@login_required
def add_pendaftaran():
    if request.method == 'POST':
        mahasiswa_id = request.form['mahasiswa_id']
        matakuliah_id = request.form['mata_kuliah_id']
        status = request.form['status']
        nilai_akhir = request.form['nilai_akhir']

        # Validasi data
        if not mahasiswa_id or not matakuliah_id:
            flash('Semua field harus diisi!', 'error')
            return redirect(url_for('admin.add_pendaftaran'))

        # Cek apakah mahasiswa sudah mendaftar mata kuliah yang sama
        existing_pendaftaran = Pendaftaran.query.filter_by(mahasiswa_id=mahasiswa_id, mata_kuliah_id=matakuliah_id).first()
        if existing_pendaftaran:
            flash('Mahasiswa sudah mendaftar mata kuliah ini!', 'error')
            return redirect(url_for('admin.add_pendaftaran'))

        # Buat objek Pendaftaran baru
        pendaftaran_baru = Pendaftaran(
            mahasiswa_id=int(mahasiswa_id),
            mata_kuliah_id=int(matakuliah_id),
            status=status,
            nilai_akhir=nilai_akhir
        )

        # Simpan ke database
        db.session.add(pendaftaran_baru)
        db.session.commit()

        flash('Pendaftaran berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.manage_pendaftaran'))
    
    # Jika metode GET, tampilkan form tambah pendaftaran
    mahasiswa_list = Mahasiswa.query.all()
    matakuliah_list = MataKuliah.query.all()
    return render_template('admin/tambah_pendaftaran.html', mahasiswa_list=mahasiswa_list, matakuliah_list=matakuliah_list)

@admin_bp.route('/edit_pendaftaran/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_pendaftaran(id):
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        mahasiswa_id = request.form['mahasiswa_id']
        matakuliah_id = request.form['mata_kuliah_id']
        status = request.form['status']
        nilai_akhir = request.form['nilai_akhir']

        # Validasi data
        if not mahasiswa_id or not matakuliah_id:
            flash('Semua field harus diisi!', 'error')
            return redirect(url_for('admin.edit_pendaftaran', id=id))

        # Cek apakah mahasiswa sudah mendaftar mata kuliah yang sama
        existing_pendaftaran = Pendaftaran.query.filter_by(mahasiswa_id=mahasiswa_id, mata_kuliah_id=matakuliah_id).first()
        if existing_pendaftaran and existing_pendaftaran.id != id:
            flash('Mahasiswa sudah mendaftar mata kuliah ini!', 'error')
            return redirect(url_for('admin.edit_pendaftaran', id=id))

        # Update data pendaftaran
        pendaftaran = Pendaftaran.query.get(id)
        pendaftaran.mahasiswa_id = int(mahasiswa_id)
        pendaftaran.mata_kuliah_id = int(matakuliah_id)
        pendaftaran.nilai_akhir = nilai_akhir
        pendaftaran.status = status

        db.session.commit()
        flash('Data pendaftaran berhasil diubah!', 'success')
        return redirect(url_for('admin.manage_pendaftaran'))
    
    # Jika metode GET, tampilkan form edit pendaftaran
    pendaftaran = Pendaftaran.query.get(id)
    mahasiswa_list = Mahasiswa.query.all()
    matakuliah_list = MataKuliah.query.all()
    return render_template('admin/edit_pendaftaran.html', pendaftaran=pendaftaran, mahasiswa_list=mahasiswa_list, matakuliah_list=matakuliah_list)

@admin_bp.route('/hapus_pendaftaran/<int:id>', methods=['GET'])
@login_required
def hapus_pendaftaran(id):
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))
    
    try:
        pendaftaran = Pendaftaran.query.get(id)
        db.session.delete(pendaftaran)
        db.session.commit()
        flash('Data pendaftaran berhasil dihapus!', 'success')
        return redirect(url_for('admin.manage_pendaftaran'))
    except:
        db.session.rollback()
        flash('Terjadi kesalahan saat menghapus data pendaftaran id {}'.format(id), 'error')

@admin_bp.route('/add_matakuliah', methods=['GET', 'POST'])
@login_required
def add_matakuliah():
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        sks = request.form['sks']
        semester = request.form['semester']
        dosen_id = request.form['dosen_id']

        # Validasi data
        if not kode or not nama or not sks or not semester or not dosen_id:
            flash('Semua field harus diisi!', 'error')
            return redirect(url_for('admin.add_matakuliah'))

        # Cek apakah kode mata kuliah sudah ada
        existing_matakuliah = MataKuliah.query.filter_by(kode=kode).first()
        if existing_matakuliah:
            flash('Kode mata kuliah sudah ada!', 'error')
            return redirect(url_for('admin.add_matakuliah'))

        # Buat objek MataKuliah baru
        matakuliah_baru = MataKuliah(
            kode=kode,
            nama=nama,
            sks=int(sks),
            semester=semester,
            dosen_id=int(dosen_id)
        )

        # Simpan ke database
        db.session.add(matakuliah_baru)
        db.session.commit()

        flash('Mata kuliah berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.manage_matakuliah'))

    # Jika metode GET, tampilkan form tambah mata kuliah
    dosen_list = Dosen.query.all()
    return render_template('admin/tambah_matakuliah.html', dosen_list=dosen_list)

@admin_bp.route('/edit_matakuliah/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_matakuliah(id):
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        sks = request.form['sks']
        semester = request.form['semester']
        dosen_id = request.form['dosen_id']

        # Validasi data
        if not kode or not nama or not sks or not semester or not dosen_id:
            flash('Semua field harus diisi!', 'error')
            return redirect(url_for('admin.edit_matakuliah', id=id))

        # Cek apakah kode mata kuliah sudah ada
        existing_matakuliah = MataKuliah.query.filter_by(kode=kode).first()
        if existing_matakuliah and existing_matakuliah.id != id:
            flash('Kode mata kuliah sudah ada!', 'error')
            return redirect(url_for('admin.edit_matakuliah', id=id))

        # Update data mata kuliah
        matakuliah = MataKuliah.query.get(id)
        matakuliah.kode = kode
        matakuliah.nama = nama
        matakuliah.sks = int(sks)
        matakuliah.semester = semester
        matakuliah.dosen_id = int(dosen_id)

        db.session.commit()
        flash('Data mata kuliah berhasil diubah!', 'success')
        return redirect(url_for('admin.manage_matakuliah'))

    # Jika metode GET, tampilkan form edit mata kuliah
    matakuliah = MataKuliah.query.get(id)
    dosen_list = Dosen.query.all()
    return render_template('admin/edit_matakuliah.html', matakuliah=matakuliah, dosen_list=dosen_list)

@admin_bp.route('/hapus_matakuliah/<int:id>', methods=['GET'])
@login_required
def hapus_matakuliah(id):
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))
    
    try:
        matakuliah = MataKuliah.query.get(id)
        db.session.delete(matakuliah)
        db.session.commit()
        flash('Data mata kuliah berhasil dihapus!', 'success')
        return redirect(url_for('admin.manage_matakuliah'))
    except:
        db.session.rollback()
        flash('Terjadi kesalahan saat menghapus data mata kuliah id {}'.format(id), 'error')
        return redirect(url_for('admin.manage_matakuliah'))

@admin_bp.route('/hapus_mahasiswa/<int:id>', methods=['GET'])
@login_required
def hapus_mahasiswa(id):
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))
    
    try:
        mahasiswa = Mahasiswa.query.get(id)
        
        if mahasiswa.pengguna_id:
            user = Pengguna.query.get(mahasiswa.pengguna_id)
            db.session.delete(user)
        
        db.session.delete(mahasiswa)
        db.session.commit()
        flash('Data mahasiswa berhasil dihapus!', 'success')
        return redirect(url_for('admin.manage_mahasiswa'))
    
    except:
        db.session.rollback()
        flash('Terjadi kesalahan saat menghapus data mahasiswa id {}'.format(id), 'error')
        return redirect(url_for('admin.manage_mahasiswa'))

@admin_bp.route('/hapus_dosen/<int:id>', methods=['GET'])
@login_required
def hapus_dosen(id):
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))
    
    try:
        dosen = Dosen.query.get(id)
        
        if dosen.pengguna_id:
            user = Pengguna.query.get(dosen.pengguna_id)
            db.session.delete(user)
        
        db.session.delete(dosen)
        db.session.commit()
        flash('Data dosen berhasil dihapus!', 'success')
        return redirect(url_for('admin.manage_dosen'))
    
    except:
        db.session.rollback()
        flash('Terjadi kesalahan saat menghapus data dosen id {}'.format(id), 'error')
        return redirect(url_for('admin.manage_dosen'))

@admin_bp.route('/edit_user/<role>/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(role, id):
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if role == 'dosen':
            nik = request.form['nik']
            nama = request.form['nama']
            tanggal_lahir = request.form['tanggal_lahir']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']
            nomor_telepon = request.form['nomor_telepon']
            spesialisasi = request.form['spesialisasi']
            
            dosen = Dosen.query.get(id)
            dosen.nik = nik
            dosen.nama = nama
            dosen.tanggal_lahir = tanggal_lahir
            dosen.jenis_kelamin = jenis_kelamin
            dosen.alamat = alamat
            dosen.nomor_telepon = nomor_telepon
            dosen.spesialisasi = spesialisasi

        elif role == 'mahasiswa':
            nim = request.form['nim']
            nama = request.form['nama']
            tanggal_lahir = request.form['tanggal_lahir']
            jenis_kelamin = request.form['jenis_kelamin']
            alamat = request.form['alamat']
            nomor_telepon = request.form['nomor_telepon']
            tahun_masuk = request.form['tahun_masuk']
            
            mahasiswa = Mahasiswa.query.get(id)
            mahasiswa.nim = nim
            mahasiswa.nama = nama
            mahasiswa.tanggal_lahir = tanggal_lahir
            mahasiswa.jenis_kelamin = jenis_kelamin
            mahasiswa.alamat = alamat
            mahasiswa.nomor_telepon = nomor_telepon
            mahasiswa.tahun_masuk = tahun_masuk

        db.session.commit()
        flash('Data berhasil diubah!', 'success')

        if role == 'dosen':
            return redirect(url_for('admin.manage_dosen'))
        elif role == 'mahasiswa':
            return redirect(url_for('admin.manage_mahasiswa'))
        
    if role == 'dosen':
        dosen = Dosen.query.get(id)
        return render_template('admin/edit_dosen.html', dosen=dosen)
    
    elif role == 'mahasiswa':
        mahasiswa = Mahasiswa.query.get(id)
        return render_template('admin/edit_mahasiswa.html', mahasiswa=mahasiswa)


    return render_template('admin/dashboard.html')

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

@admin_bp.route('/hapus_user/<int:id>', methods=['GET'])
@login_required
def hapus_user(id):
    if current_user.peran != 'admin':
        return redirect(url_for('auth.login'))
    
    try:
        user = Pengguna.query.get(id)
        db.session.delete(user)
        db.session.commit()
        flash('Akun berhasil dihapus!', 'success')
    except:
        flash('Terjadi kesalahan saat menghapus akun id {}'.format(id), 'error')

    return redirect(url_for('admin.manage_users'))