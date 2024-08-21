class Config:
    USERNAME = 'root'
    PASSWORD = ''
    HOST = 'localhost'
    DATABASE = 'sertikom_db'

    SECRET_KEY = 'asdasa'
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False