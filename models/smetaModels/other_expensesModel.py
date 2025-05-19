from extentions.db import db

class other_exp_model(db.Model):
    __tablename__ = 'other_expenses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_code = db.Column(db.Integer, nullable=False)
    expenses_name = db.Column(db.String, nullable=False)
    unit_of_measure = db.Column(db.String, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)

    def others(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'expenses_name': self.expenses_name,
            'unit_of_measure': self.unit_of_measure,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'duration': self.duration,
            'total_amount': self.total_amount
        }
