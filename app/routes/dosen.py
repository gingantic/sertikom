from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from app.models import Dosen
from ..utils import peran_required

dosen_bp = Blueprint('dosen', __name__)

@dosen_bp.route('/dosen/dashboard')
@login_required
def dashboard():

    if current_user.peran != 'dosen':
        flash(f'Anda tidak memiliki akses ke halaman {url_for(request.endpoint)}.', 'error')
        return redirect(url_for(f'{current_user.peran}.dashboard'))
    
    return render_template('dosen/dashboard.html')

# @dosen_bp.route('/detail')
# @login_required
# @peran_required('dosen')
# def detail():
#     dosen = Dosen.query.filter_by(pengguna_id=current_user.id).first()
#     return render_template('dosen/detail.html', dosen=dosen)
