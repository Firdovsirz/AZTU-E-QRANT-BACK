from flask import Blueprint, request, jsonify
from models.salaryModel import db, Salary

salary_bp = Blueprint('salary_bp', __name__)


@salary_bp.route('/api/create-salary-table', methods=['POST'])
def add_salary():
    data = request.get_json()

    try:
        new_salary = Salary(
            project_code=data['project_code'],
            full_name=data['full_name'],
            project_function=data['project_function'],
            salary_per_month=data['salary_per_month'],
            months=data['months'],
            total_salary=data['total_salary']
        )
        db.session.add(new_salary)
        db.session.commit()
        return jsonify({'message': 'Salary record created', 'data': new_salary.salarytable()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@salary_bp.route('/api/all-salaries-table', methods=['GET'])
def get_all_salaries():
    salaries = Salary.query.all()
    return jsonify([s.salarytable() for s in salaries]), 200



@salary_bp.route('/api/edit-salary-table/<int:project_code>', methods=['PATCH'])
def update_salary(project_code):
    data = request.get_json()
    salary = Salary.query.get(project_code)

    if not salary:
        return jsonify({'message': 'Salary record not found'}), 404

    try:
        if 'project_code' in data:
            salary.project_code = data['project_code']
        if 'full_name' in data:
            salary.full_name = data['full_name']
        if 'project_function' in data:
            salary.project_function = data['project_function']
        if 'salary_per_month' in data:
            salary.salary_per_month = data['salary_per_month']
        if 'months' in data:
            salary.months = data['months']
        if 'total_salary' in data:
            salary.total_salary = data['total_salary']

        db.session.commit()
        return jsonify({'message': 'Salary record updated', 'data': salary.salarytable()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@salary_bp.route('/api/salary/<int:project_code>', methods=['DELETE'])
def delete_salary(project_code):
    salary = Salary.query.get(project_code)
    if not salary:
        return jsonify({'message': 'Salary record not found'}), 404

    try:
        db.session.delete(salary)
        db.session.commit()
        return jsonify({'message': 'Salary record deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
