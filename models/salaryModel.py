from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Salary(db.Model):
    __tablename__ = 'salary_table'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_code = db.Column(db.Integer, db.ForeignKey('project.project_code'), primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    project_function = db.Column(db.String, nullable=False)
    salary_per_month = db.Column(db.Integer, nullable=False)
    months = db.Column(db.Integer, nullable=False)
    total_salary = db.Column(db.Integer, nullable=False)

    def salarytable (self):
        return {
            'id': self.id,
            'project_code': self.project_code,
            'full_name': self.full_name,
            'project_function': self.project_function,
            'salary_per_month': self.salary_per_month,
            'months': self.months,
            'total_salary':self.total_salary
        }
