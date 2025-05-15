from flask import Blueprint, request, jsonify
from models.projectModel import Project  
from models.servicesTableModel import db, ServicesOfPurchase

services_bp = Blueprint('services_bp', __name__)

@services_bp.route('/api/add-services', methods=['POST'])
def add_subject():
    data = request.get_json()
    try:
        matching_project = Project.query.filter_by(
            project_code=data['project_code'],
            fin_kod=data['fin_code']
        ).first()

        if not matching_project:
            return jsonify({'error': 'No matching project found with given project_code and fin_code'}), 400

        new_subject = ServicesOfPurchase(
            project_code=data['project_code'],
            fin_code=data['fin_code'],
            services_name=data['services_name'],
            unit_of_measure=data['unit_of_measure'],
            price=data['price'],
            quantity=data['quantity'],
            total_amount=data['price'] * data['quantity']
        )
        db.session.add(new_subject)
        db.session.commit()
        return jsonify({'message': 'Subject added successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@services_bp.route('/api/get-services', methods=['GET'])
def get_subjects():
    try:
        
        results = db.session.query(ServicesOfPurchase).join(
            Project,
            (ServicesOfPurchase.project_code == Project.project_code) &
            (ServicesOfPurchase.fin_code == Project.fin_kod)
        ).all()

        response = [{
            'project_code': s.project_code,
            'fin_code': s.fin_code,
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
def update_subject(project_code):
    data = request.get_json()

    try:
        subject = ServicesOfPurchase.query.get(project_code)

        if not subject:
            return jsonify({'error': 'Subject not found with the provided ID'}), 404
        if 'services_name' in data:
            subject.services_name = data['services_name']
        if 'unit_of_measure' in data:
            subject.unit_of_measure = data['unit_of_measure']
        if 'price' in data:
            subject.price = data['price']
        if 'quantity' in data:
            subject.quantity = data['quantity']
        if 'price' in data or 'quantity' in data:

            subject.total_amount = subject.price * subject.quantity

        db.session.commit()
        return jsonify({'message': 'Subject updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    

@services_bp.route('/api/delete-services/<int:project_code>', methods=['DELETE'])
def delete_subject(project_code):
    try:
        subject = ServicesOfPurchase.query.get(project_code) 

        if not subject:
            return jsonify({'error': 'Subject not found with the provided ID'}), 404

        db.session.delete(subject)
        db.session.commit()
        return jsonify({'message': 'Subject deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

