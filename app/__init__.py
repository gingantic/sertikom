from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import *

login_manager = LoginManager()

app = Flask(__name__)

def create_app():

    # Konfigurasi aplikasi
    app.config.from_object('config.Config')

    # Konfigurasi login manager
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # Konfigurasi database
    with app.app_context():
        db.create_all()
    
    # Import dan daftarkan blueprints
    from .routes.auth import auth_bp
    from .routes.mahasiswa import mahasiswa_bp
    from .routes.dosen import dosen_bp
    from .routes.mata_kuliah import mata_kuliah_bp
    from .routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(mahasiswa_bp)
    app.register_blueprint(dosen_bp)
    app.register_blueprint(mata_kuliah_bp)
    app.register_blueprint(admin_bp)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    return Pengguna.query.get(int(user_id))
