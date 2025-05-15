from flask import Blueprint, request, jsonify
from models.smetaModels.smetaModel import db, Smeta

smeta_bp = Blueprint('smeta_bp', __name__)

# ➕ POST - Create new smeta record
@smeta_bp.route('/api/create-smeta', methods=['POST'])
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


@smeta_bp.route('/api/all-smeta', methods=['GET'])
def get_all_smeta():
    smetas = Smeta.query.all()
    return jsonify([s.serialize() for s in smetas]), 200
 


@smeta_bp.route('/apiedit-smeta/<int:project_code>', methods=['PATCH'])
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
