import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
        # 'postgresql://rzaev:sonoma89@localhost:5432/zefer-hesabat'
        # env olmadan yuxaridaki versiya
    SQLALCHEMY_TRACK_MODIFICATIONS = False