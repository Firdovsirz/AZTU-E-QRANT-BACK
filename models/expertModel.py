from extentions.db import db
from flask_sqlalchemy import SQLAlchemy

class Expert(db.Model):
    __tablename__ = 'experts'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    father_name = db.Column(db.Text, nullable=False)
    personal_id_serial_number = db.Column(db.Text, nullable=False, unique=True)
    work_place = db.Column(db.Text)
    duty = db.Column(db.Text)
    scientific_degree = db.Column(db.Text)
    phone_number = db.Column(db.Text)