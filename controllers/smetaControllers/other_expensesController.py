from flask import Blueprint, request, jsonify
from utils.jwt_required import token_required
from models.smetaModels.other_expensesModel import db, other_exp_model

other_exp = Blueprint('other_exp', __name__)


@other_exp.route('/api/other_exp', methods=['POST'])
@token_required([0])
def create_other_exp():
    data = request.get_json()
    try:
        new_other_exp = other_exp_model(
            project_code=data['project_code'],
            expenses_name=data['expenses_name'],
            unit_of_measure=data['unit_of_measure'],
            unit_price=data['unit_price'],
            quantity=data['quantity'],
            duration=data['duration'],
            total_amount=data['total_amount']
        )
        db.session.add(new_other_exp)
        db.session.commit()
        return jsonify({'message': 'other_exp record created', 'data': new_other_exp.others()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@other_exp.route('/api/get-other_exp-all-tables/<int:project_code>', methods=['GET'])
@token_required([0, 1])
def get_all_other_exps(project_code):
    other_exps = other_exp_model.query.filter_by(project_code=project_code).all()
    return jsonify([r.others() for r in other_exps]), 200




@other_exp.route('/api/edit-other_exp-table/<int:id>', methods=['PATCH'])
@token_required([0])
def update_other_exp(id):
    data = request.get_json()
    other_exp = other_exp.query.get(id)

    if not other_exp:
        return jsonify({'message': 'other_exp record not found'}), 404

    try:
        if 'project_code' in data:
            other_exp.project_code = data['project_code']
        if 'expenses_name' in data:
            other_exp.expenses_name = data['expenses_name']
        if 'unit_of_measure' in data:
            other_exp.unit_of_measure = data['unit_of_measure']
        if 'unit_price' in data:
            other_exp.unit_price = data['unit_price']
        if 'quantity' in data:
            other_exp.quantity = data['quantity']
        if 'duration' in data:
            other_exp.duration = data['duration']
        if 'total_amount' in data:
            other_exp.total_amount = data['total_amount']

        db.session.commit()
        return jsonify({'message': 'other_exp record updated', 'data': other_exp.other_exp()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@other_exp.route('/api/delete-other_exp-table/<int:project_code>/<int:id>', methods=['DELETE'])
@token_required([0])
def delete_other_exp(project_code, id):
    record = other_exp_model.query.filter_by(project_code=project_code, id=id).first()
    if not record:
        return jsonify({'message': 'other_exp record not found'}), 404

    try:
        db.session.delete(record)
        db.session.commit()
        return jsonify({'message': 'other_exp record deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
