from extentions.db import db
from flask_sqlalchemy import SQLAlchemy

class Collaborator(db.Model):
    __tablename__ = 'Collaborators'

    id = db.Column(db.Integer, primary_key=True)
    project_code = db.Column(db.Integer, unique=True, nullable=False)
    fin_kod = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return str([
            {"id": self.id}, 
            {"project_code": self.project_code}, 
            {"fin_kod": self.fin_kod}
        ])