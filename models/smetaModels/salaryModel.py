from extentions.db import db

class Salary(db.Model):
    __tablename__ = 'salary_smeta'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_code = db.Column(db.Integer, primary_key=True)
    fin_kod = db.Column(db.Text, nullable=False)
    salary_per_month = db.Column(db.Integer, nullable=False)
    months = db.Column(db.Integer, nullable=False)
    total_salary = db.Column(db.Integer, nullable=False)

    def salary_details(self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'fin_kod': self.fin_kod,
            'salary_per_month': self.salary_per_month,
            'months': self.months,
            'total_salary':self.total_salary
        }
