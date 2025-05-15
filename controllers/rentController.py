from flask import Blueprint, request, jsonify
from models.rentModel import db, Rent

rent_bp = Blueprint('rent_bp', __name__)


@rent_bp.route('/api/rent', methods=['POST'])
def create_rent():
    data = request.get_json()
    try:
        new_rent = Rent(
            project_code=data['project_code'],
            rent_area=data['rent_area'],
            unit_of_measure=data['unit_of_measure'],
            unit_price=data['unit_price'],
            quantity=data['quantity'],
            duration=data['duration'],
            total_amount=data['total_amount']
        )
        db.session.add(new_rent)
        db.session.commit()
        return jsonify({'message': 'Rent record created', 'data': new_rent.rent()}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@rent_bp.route('/api/get-rent-all-tables', methods=['GET'])
def get_all_rents():
    rents = Rent.query.all()
    return jsonify([r.rent() for r in rents]), 200




@rent_bp.route('/api/edit-rent-table/<int:id>', methods=['PATCH'])
def update_rent(id):
    data = request.get_json()
    rent = Rent.query.get(id)

    if not rent:
        return jsonify({'message': 'Rent record not found'}), 404

    try:
        if 'project_code' in data:
            rent.project_code = data['project_code']
        if 'rent_area' in data:
            rent.rent_area = data['rent_area']
        if 'unit_of_measure' in data:
            rent.unit_of_measure = data['unit_of_measure']
        if 'unit_price' in data:
            rent.unit_price = data['unit_price']
        if 'quantity' in data:
            rent.quantity = data['quantity']
        if 'duration' in data:
            rent.duration = data['duration']
        if 'total_amount' in data:
            rent.total_amount = data['total_amount']

        db.session.commit()
        return jsonify({'message': 'Rent record updated', 'data': rent.rent()}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@rent_bp.route('/api/delete-rent-table/<int:project_code>', methods=['DELETE'])
def delete_rent(project_code):
    rent = Rent.query.get(project_code)
    if not rent:
        return jsonify({'message': 'Rent record not found'}), 404

    try:
        db.session.delete(rent)
        db.session.commit()
        return jsonify({'message': 'Rent record deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400
