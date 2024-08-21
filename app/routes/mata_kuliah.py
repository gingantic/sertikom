from flask import Blueprint, render_template
from flask_login import login_required
from app.models import MataKuliah

mata_kuliah_bp = Blueprint('mata_kuliah', __name__)

@mata_kuliah_bp.route('/')
@login_required
def index():
    mata_kuliah_list = MataKuliah.query.all()
    return render_template('mata_kuliah/index.html', mata_kuliah=mata_kuliah_list)

@mata_kuliah_bp.route('/detail/<int:mata_kuliah_id>')
@login_required
def detail(mata_kuliah_id):
    mata_kuliah = MataKuliah.query.get_or_404(mata_kuliah_id)
    return render_template('mata_kuliah/detail.html', mata_kuliah=mata_kuliah)
