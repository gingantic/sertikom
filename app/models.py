from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

# Model untuk tabel `pengguna`
class Pengguna(db.Model, UserMixin):
    __tablename__ = 'pengguna'
    
    id = db.Column(db.Integer, primary_key=True)
    nama_pengguna = db.Column(db.String(80), unique=True, nullable=False)
    kata_sandi = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    peran = db.Column(db.Enum('admin', 'dosen', 'mahasiswa', name='peran_enum'), nullable=False)
    dibuat_pada = db.Column(db.DateTime, default=datetime.utcnow)
    diperbarui_pada = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    mahasiswa = db.relationship('Mahasiswa', backref='pengguna', uselist=False)
    dosen = db.relationship('Dosen', backref='pengguna', uselist=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'kata_sandi':
                value = generate_password_hash(value)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

# Model untuk tabel `mahasiswa`
class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa'
    
    id = db.Column(db.Integer, primary_key=True)
    pengguna_id = db.Column(db.Integer, db.ForeignKey('pengguna.id'), nullable=False)
    nim = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(120), nullable=False)
    tanggal_lahir = db.Column(db.Date, nullable=False)
    jenis_kelamin = db.Column(db.Enum('pria', 'wanita', name='jenis_kelamin_enum'), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    nomor_telepon = db.Column(db.String(15), nullable=False)
    tahun_masuk = db.Column(db.Integer, nullable=False)
    
    pendaftaran = db.relationship('Pendaftaran', backref='mahasiswa', lazy=True)

# Model untuk tabel `dosen`
class Dosen(db.Model):
    __tablename__ = 'dosen'
    
    id = db.Column(db.Integer, primary_key=True)
    pengguna_id = db.Column(db.Integer, db.ForeignKey('pengguna.id'), nullable=False)
    nik = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(120), nullable=False)
    spesialisasi = db.Column(db.String(120), nullable=False)
    tanggal_lahir = db.Column(db.Date, nullable=False)
    jenis_kelamin = db.Column(db.Enum('pria', 'wanita', name='jenis_kelamin_enum'), nullable=False)
    alamat = db.Column(db.Text, nullable=False)
    nomor_telepon = db.Column(db.String(15), nullable=False)
    
    mata_kuliah = db.relationship('MataKuliah', backref='dosen', lazy=True)

# Model untuk tabel `mata_kuliah`
class MataKuliah(db.Model):
    __tablename__ = 'mata_kuliah'
    
    id = db.Column(db.Integer, primary_key=True)
    kode = db.Column(db.String(20), unique=True, nullable=False)
    nama = db.Column(db.String(120), nullable=False)
    sks = db.Column(db.Integer, nullable=False)
    semester = db.Column(db.Enum('1', '2', '3', '4', '5', '6', '7', '8', name='semester_enum'), nullable=False)
    dosen_id = db.Column(db.Integer, db.ForeignKey('dosen.id'), nullable=False)
    dibuat_pada = db.Column(db.DateTime, default=datetime.utcnow)
    diperbarui_pada = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    pendaftaran = db.relationship('Pendaftaran', backref='mata_kuliah', lazy=True)
    jadwal = db.relationship('Jadwal', backref='mata_kuliah', lazy=True)

# Model untuk tabel `pendaftaran`
class Pendaftaran(db.Model):
    __tablename__ = 'pendaftaran'
    
    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    mata_kuliah_id = db.Column(db.Integer, db.ForeignKey('mata_kuliah.id'), nullable=False)
    tanggal_pendaftaran = db.Column(db.DateTime, default=datetime.utcnow)
    nilai_akhir = db.Column(db.String(4))
    status = db.Column(db.Enum('aktif', 'selesai', 'batal', name='status_enum'), nullable=False)

# Model untuk tabel `jadwal`
class Jadwal(db.Model):
    __tablename__ = 'jadwal'
    
    id = db.Column(db.Integer, primary_key=True)
    mata_kuliah_id = db.Column(db.Integer, db.ForeignKey('mata_kuliah.id'), nullable=False)
    hari = db.Column(db.Enum('Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', name='hari_enum'), nullable=False)
    waktu_mulai = db.Column(db.Time, nullable=False)
    waktu_selesai = db.Column(db.Time, nullable=False)
    ruang = db.Column(db.String(50), nullable=False)
