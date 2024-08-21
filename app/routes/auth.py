from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Pengguna
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        if current_user.peran == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.peran == 'dosen':
            return redirect(url_for('dosen.dashboard'))
        elif current_user.peran == 'mahasiswa':
            return redirect(url_for('mahasiswa.dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pengguna = Pengguna.query.filter_by(nama_pengguna=username).first()
        if pengguna and check_password_hash(pengguna.kata_sandi, password):
            login_user(pengguna)

            if pengguna.peran == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif pengguna.peran == 'dosen':
                return redirect(url_for('dosen.dashboard'))
            elif pengguna.peran == 'mahasiswa':
                return redirect(url_for('mahasiswa.dashboard'))
            
        flash('Username atau password salah', 'error')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    flash('Anda telah logout', 'success')

    logout_user()
    return redirect(url_for('auth.login'))

# @auth_bp.route('/register', methods=['GET', 'POST'])
# @login_required
# def register():
#     if current_user.peran != 'admin':
#         return redirect(url_for('auth.login'))
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         email = request.form['email']
#         role = request.form['role']
#         hashed_password = generate_password_hash(password)

#         pengguna = Pengguna(nama_pengguna=username, kata_sandi=hashed_password, email=email, peran=role)
#         db.session.add(pengguna)
#         db.session.commit()
#         flash('Pengguna berhasil didaftarkan', 'success')
#         return redirect(url_for('auth.login'))
#     return render_template('auth/register.html')

@auth_bp.route('/reg_admin', methods=['POST'])
def reg_admin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    role = 'admin'
    
    if 'role' in data:
        role = data.get('role')

    if not username or not password or not email:
        return {'message': 'Semua field harus diisi'}, 400

    pengguna = Pengguna(nama_pengguna=username, kata_sandi=password, email=email, peran=role)

    db.session.add(pengguna)
    db.session.commit()

    return {'message': 'Admin berhasil didaftarkan'}, 201

