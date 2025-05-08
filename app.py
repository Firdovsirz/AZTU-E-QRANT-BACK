from flask import Flask
from flask_cors import CORS
from extentions.db import db
from config.config import Config

def main_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins="*")

    db.init_app(app)

    with app.app_context():
        db.create_all()