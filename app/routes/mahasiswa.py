from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from app.models import Mahasiswa

mahasiswa_bp = Blueprint('mahasiswa', __name__)

@mahasiswa_bp.route('/mahasiswa/dashboard')
@login_required
def dashboard():
    if current_user.peran != 'mahasiswa':
        flash(f'Anda tidak memiliki akses ke halaman {url_for(request.endpoint)}.', 'error')
        return redirect(url_for(f'{current_user.peran}.dashboard'))
    
    return render_template('mahasiswa/dashboard.html')