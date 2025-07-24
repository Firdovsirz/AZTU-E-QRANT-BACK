from extentions.db import db
from flask_sqlalchemy import SQLAlchemy

class Priotet(db.Model):
    __tablename__ = 'prioritets'

    id = db.Column(db.Integer, primary_key=True)
    prioritet_name = db.Column(db.Text, nullable=False)
    prioritet_code = db.Column(db.Integer, nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False)