from extentions.db import db

class Smeta(db.Model):
    __tablename__ = 'smeta'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_code = db.Column(db.Integer, nullable=False, unique=True)
    total_salary = db.Column(db.Integer)
    total_fee = db.Column(db.Integer)
    defense_fund = db.Column(db.Integer)
    total_equipment = db.Column(db.Integer)
    total_services = db.Column(db.Integer)
    total_rent = db.Column(db.Integer)
    other_expenses = db.Column(db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'total_salary': self.total_salary,
            'total_fee': self.total_fee,
            'defense_fund': self.defense_fund,
            'total_equipment': self.total_equipment,
            'total_services': self.total_services,
            'total_rent': self.total_rent,
            'other_expenses': self.other_expenses
        }
