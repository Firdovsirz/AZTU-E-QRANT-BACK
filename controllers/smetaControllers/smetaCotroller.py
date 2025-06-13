from models.projectModel import Project
from utils.jwt_required import token_required
from flask import Blueprint, request, jsonify
from models.smetaModels.rentModel import Rent
from models.smetaModels.salaryModel import Salary
from models.smetaModels.smetaModel import db, Smeta
from models.smetaModels.subjectModel import SubjectOfPurchase
from models.smetaModels.other_expensesModel import other_exp_model
from models.smetaModels.servicesTableModel import ServicesOfPurchase
from exceptions.exception import handle_specific_not_found, handle_global_exception, handle_success

smeta_bp = Blueprint('smeta_bp', __name__)

# ➕ POST - Create new smeta record
@smeta_bp.route('/api/create-smeta', methods=['POST'])
@token_required([1])
def create_smeta():
    data = request.get_json()
    try:
        new_smeta = Smeta(
            project_code=data['project_code'],
            total_salary=data['total_salary'],
            total_fee=data['total_fee'],
            defense_fund=data['defense_fund'],
            total_equipment=data['total_equipment'],
            total_services=data['total_services'],
            total_rent=data['total_rent'],
            other_expenses=data.get('other_expenses')
        )
        db.session.add(new_smeta)
        db.session.commit()
        return jsonify({'message': 'Smeta created', 'data': new_smeta.serialize()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@smeta_bp.route("/api/main-smeta/<int:project_code>", methods=['GET'])
@token_required([1])
def get_main_smeta_by_project_code(project_code):

    try:

        project = Project.query.filter_by(project_code=project_code).first()

        if not project:
             return handle_specific_not_found("Project not found for the project code.")
        
        total_salary_smeta = Salary.query.filter_by(project_code=project_code).all()

        total_salary_amount = 0

        for i in total_salary_smeta:
            total_salary_amount += i.total_salary


        total_tools_smeta = SubjectOfPurchase.query.filter_by(project_code=project_code).all()

        total_tools_amount = 0

        for i in total_tools_smeta:
            total_tools_amount += i.total_amount

        total_services_smeta = ServicesOfPurchase.query.filter_by(project_code=project_code).all()

        total_services_amount = 0

        for i in total_services_smeta:
            total_services_amount += i.total_amount

        total_rent_smeta = Rent.query.filter_by(project_code=project_code).all()

        total_rent_amount = 0

        for i in total_rent_smeta:

            total_rent_amount += i.total_amount

        total_other_smeta = other_exp_model.query.filter_by(project_code=project_code).all()

        total_other_amount = 0

        for i in total_other_smeta:

            total_other_amount += i.total_amount

        main_smeta_data = {
            "total_salary_smeta": total_salary_amount,
            "total_tools_smeta": total_tools_amount,
            "total_services_smeta": total_services_amount,
            "total_rent_smeta": total_rent_amount,
            "total_other_smeta": total_other_amount
        }

        return handle_success(main_smeta_data, "Smeta fetched successfully.")
    
    except Exception as e:
        return handle_global_exception(str(e))

@smeta_bp.route('/api/edit-smeta/<int:project_code>', methods=['PATCH'])
@token_required([1])
def update_smeta(project_code):
    data = request.get_json()
    smeta = Smeta.query.get(project_code)

    if not smeta:
        return jsonify({'message': 'Smeta not found'}), 404

    try:
        for field in ['total_salary', 'total_fee', 'defense_fund', 'total_equipment', 'total_services', 'total_rent', 'other_expenses']:
            if field in data:
                setattr(smeta, field, data[field])

        db.session.commit()
        return jsonify({'message': 'Smeta updated', 'data': smeta.serialize()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@smeta_bp.route('/api/delete-smeta/<int:project_code>', methods=['DELETE'])
@token_required([1])
def delete_smeta(project_code):
    smeta = Smeta.query.get(project_code)
    if not smeta:
        return jsonify({'message': 'Smeta not found'}), 404

    try:
        db.session.delete(smeta)
        db.session.commit()
        return jsonify({'message': 'Smeta deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
