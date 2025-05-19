from extentions.db import db
from flask_sqlalchemy import SQLAlchemy

class Collaborator(db.Model):
    __tablename__ = 'collaborators'

    id = db.Column(db.Integer, primary_key=True)
    project_code = db.Column(db.Integer, nullable=False)
    fin_kod = db.Column(db.String, unique=True, nullable=False)


    
    def collaboraator_details(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'fin_code': self.fin_kod    
        }