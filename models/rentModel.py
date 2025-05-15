from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Rent(db.Model):
    __tablename__ = 'rent_table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_code = db.Column(db.Integer, nullable=False)
    rent_area = db.Column(db.String, nullable=False)
    unit_of_measure = db.Column(db.String, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)

    def rent(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'rent_area': self.rent_area,
            'unit_of_measure': self.unit_of_measure,
            'unit_price': self.unit_price,
            'quantity': self.quantity,
            'duration': self.duration,
            'total_amount': self.total_amount
        }
