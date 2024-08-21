from flask import Blueprint

# Inisialisasi semua blueprints
auth_bp = Blueprint('auth', __name__)
mahasiswa_bp = Blueprint('mahasiswa', __name__)
dosen_bp = Blueprint('dosen', __name__)
mata_kuliah_bp = Blueprint('mata_kuliah', __name__)
admin_bp = Blueprint('admin', __name__)
