from models.userModel import User
from models.projectModel import Project
from flask import Blueprint, request, jsonify
from models.collaboratorModel import Collaborator
from models.smetaModels.salaryModel import db, Salary
from exceptions.exception import handle_specific_not_found, handle_global_exception
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

salary_bp = Blueprint('salary_bp', __name__)


@salary_bp.route('/api/create-salary-table', methods=['POST'])
def add_salary():
    data = request.get_json()
    logger.debug("Received request data: %s", data)

    try:
        salary_per_month = data.get('salary_per_month')
        months = data.get('months')

        # Type and null checks with clear logging
        if salary_per_month is None or months is None:
            logger.error("Missing salary_per_month or months. Data: %s", data)
            return jsonify({'error': 'Missing salary_per_month or months'}), 400

        try:
            salary_per_month = int(salary_per_month)
            months = int(months)
        except ValueError:
            logger.error("Invalid input types: salary_per_month=%s (type=%s), months=%s (type=%s)",
                         salary_per_month, type(salary_per_month), months, type(months))
            return jsonify({'error': 'Invalid input types'}), 400

        logger.debug("Parsed salary_per_month: %s, months: %s", salary_per_month, months)

        total_salary = salary_per_month * months
        logger.debug("Calculated total_salary: %s", total_salary)

        logger.debug("Creating Salary with project_code=%s, fin_kod=%s", data['project_code'], data['fin_kod'])
        new_salary = Salary(
            project_code=data['project_code'],
            fin_kod=data['fin_kod'],
            salary_per_month=salary_per_month,
            months=months,
            total_salary=total_salary
        )

        logger.debug("New Salary object: %s", new_salary.salary_details())
        db.session.add(new_salary)
        db.session.commit()

        return jsonify({'message': 'Salary record created', 'data': new_salary.salary_details()}), 201
    except Exception as e:
        logger.exception("Error occurred while creating salary record")
        return jsonify({'error': str(e)}), 400


@salary_bp.route("/api/salary/smeta/<int:project_code>", methods=['GET'])
def get_salary_smeta_by_project_code(project_code):
    logger.debug("Fetching salary smeta for project_code: %s", project_code)
    try:
        # Get the project
        project = Project.query.filter_by(project_code=project_code).first()
        if not project:
            return handle_specific_not_found('Project not found')

        # Get project owner info
        project_owner_user = User.query.filter_by(fin_kod=project.fin_kod).first()
        project_owner_salary = Salary.query.filter_by(project_code=project_code, fin_kod=project.fin_kod).first()

        project_owner_data = {
            "fin_kod": project.fin_kod,
            "name": project_owner_user.name if project_owner_user else None,
            "surname": project_owner_user.surname if project_owner_user else None,
            "father_name": project_owner_user.father_name if project_owner_user else None,
            "salary": project_owner_salary.salary_details() if project_owner_salary else None,
        }

        # Get collaborators
        collaborators = Collaborator.query.filter_by(project_code=project_code).all()
        collaborator_list = []

        for collaborator in collaborators:
            user = User.query.filter_by(fin_kod=collaborator.fin_kod).first()
            salary = Salary.query.filter_by(project_code=project_code, fin_kod=collaborator.fin_kod).first()

            collaborator_list.append({
                "fin_kod": collaborator.fin_kod,
                "name": user.name if user else None,
                "surname": user.surname if user else None,
                "father_name": user.father_name if user else None,
                "salary": salary.salary_details() if salary else None
            })

        return jsonify({
            "project_owner": project_owner_data,
            "collaborators": collaborator_list
        })

    except Exception as e:
        logger.exception("Error occurred while fetching salary smeta")
        return handle_global_exception(str(e))

@salary_bp.route('/api/all-salaries-table', methods=['GET'])
def get_all_salaries():
    salaries = Salary.query.all()
    return jsonify([s.salarytable() for s in salaries]), 200



@salary_bp.route('/api/edit-salary-table/<int:project_code>', methods=['PATCH'])
def update_salary(project_code):
    data = request.get_json()
    
    salary = Salary.query.filter_by(project_code=project_code).first()

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



@salary_bp.route('/api/delete-salary/<int:project_code>', methods=['DELETE'])
def delete_salary(project_code):
    salary = Salary.query.filter_by(project_code=project_code).first()

    if not salary:
        return jsonify({'message': 'Salary record not found'}), 404

    try:
        db.session.delete(salary)
        db.session.commit()
        return jsonify({'message': 'Salary record deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
