import logging
from models.projectModel import Project  
from utils.jwt_required import token_required
from flask import Blueprint, request, jsonify
from models.smetaModels.servicesTableModel import db, ServicesOfPurchase

logging.basicConfig(level=logging.DEBUG)

services_bp = Blueprint('services_bp', __name__)

@services_bp.route('/api/add-services', methods=['POST'])
@token_required([1])
def add_subject():
    data = request.get_json()
    logging.debug(f"Received data: {data}")
    try:
        matching_project = Project.query.filter_by(
            project_code=data['project_code']
        ).first()

        if not matching_project:
            logging.debug("No matching project found.")
            return jsonify({'error': 'No matching project found with given project_code and fin_code'}), 400

        new_subject = ServicesOfPurchase(
            project_code=data['project_code'],
            services_name=data['services_name'],
            unit_of_measure=data['unit_of_measure'],
            price=data['price'],
            quantity=data['quantity'],
            total_amount=data['price'] * data['quantity']
        )
        db.session.add(new_subject)
        db.session.commit()
        logging.debug("New subject added successfully.")
        return jsonify({'message': 'Subject added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        logging.exception("Exception occurred while adding subject:")
        return jsonify({'error': str(e)}), 400


@services_bp.route('/api/get-services/<int:project_code>', methods=['GET'])
@token_required([1])
def get_subjects(project_code):
    try:
        results = ServicesOfPurchase.query.filter_by(project_code=project_code).all()

        response = [{
            'project_code': s.project_code,
            'services_name': s.services_name,
            'unit_of_measure': s.unit_of_measure,
            'price': s.price,
            'quantity': s.quantity,
            'total_amount': s.total_amount
        } for s in results]

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400



@services_bp.route('/api/update-services/<int:project_code>', methods=['PATCH'])
@token_required([1])
def update_subject(project_code):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'Invalid or missing JSON data'}), 400

        services = ServicesOfPurchase.query.get(project_code)

        if not services:
            return jsonify({'error': 'Service not found with the provided ID'}), 404

        # Update only if the fields exist
        if 'services_name' in data:
            services.services_name = data['services_name']
        if 'unit_of_measure' in data:
            services.unit_of_measure = data['unit_of_measure']
        if 'price' in data:
            services.price = data['price']
        if 'quantity' in data:
            services.quantity = data['quantity']

        # Recalculate total_amount only if both values are available and valid
        if services.price is not None and services.quantity is not None:
            try:
                services.total_amount = float(services.price) * float(services.quantity)
            except Exception as e:
                return jsonify({'error': f"Calculation error: {str(e)}"}), 400

        db.session.commit()
        return jsonify({'message': 'Service updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Server error: {str(e)}"}), 500


    

@services_bp.route('/api/delete-services/<int:project_code>', methods=['DELETE'])
@token_required([1])
def delete_subject(project_code):
    services = ServicesOfPurchase.query.filter_by(project_code=project_code).first()

    if not services:
        return jsonify({'message': 'services not found'}), 404

    try:
        db.session.delete(services)
        db.session.commit()
        return jsonify({'message': 'services deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400