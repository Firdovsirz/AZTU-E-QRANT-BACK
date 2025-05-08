from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    surname = db.Column(db.Text, nullable=False)
    father_name = db.Column(db.Text, nullable=False)
    fin_kod = db.Column(db.Text, unique=True, nullable=False)
    image = db.Column(db.LargeBinary)
    born_place = db.Column(db.Text, nullable=False)
    living_location = db.Column(db.Text, nullable=False)
    home_phone = db.Column(db.Text, unique=True, nullable=False)
    personal_mobile_number = db.Column(db.Text, unique=True, nullable=False)
    personal_email = db.Column(db.Text, unique=True, nullable=False)
    citizenship = db.Column(db.Text, nullable=False)
    personal_id_number = db.Column(db.Text, nullable=False)
    sex = db.Column(db.Text, nullable=False)
    work_place = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=False)
    duty = db.Column(db.Text, nullable=False)
    main_education = db.Column(db.Text, nullable=False)
    additonal_education = db.Column(db.Text)
    scientific_degree = db.Column(db.Text, nullable=False)
    scientific_date = db.Column(db.DateTime, nullable=False)
    scientific_name = db.Column(db.Text, nullable=False)
    scientific_name_date = db.Column(db.DateTime, nullable=False)
    work_location = db.Column(db.Text, nullable=False)
    work_phone = db.Column(db.Text, unique=True, nullable=False)
    work_email = db.Column(db.Text, unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name} {self.surname}>"