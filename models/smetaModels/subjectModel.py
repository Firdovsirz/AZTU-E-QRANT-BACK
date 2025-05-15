from extentions.db import db

class SubjectOfPurchase(db.Model):
    __tablename__ = 'subject_of_purchase'


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_code = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.Text, nullable=False)
    unit_of_measure = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)

    def subject_details(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'equipment_name': self.equipment_name,
            'unit_of_measure': self.unit_of_measure,
            'price': self.price,
            'quantity': self.quantity,
            'total_amount': self.total_amount
        }
