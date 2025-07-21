from models.projectModel import Project
from utils.jwt_required import token_required
from flask import Blueprint, request, jsonify
from models.smetaModels.subjectModel import db, SubjectOfPurchase
from exceptions.exception import handle_success, handle_global_exception
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

subject_bp = Blueprint('subject_bp', __name__)

@subject_bp.route('/api/add-subject', methods=['POST'])
@token_required([0])
def add_subject():
    data = request.get_json()
    logger.debug(f"Received data for add_subject: {data}")
    try:
        matching_project = Project.query.filter_by(
            project_code=data['project_code'],
            fin_kod=data['fin_code']
        ).first()

        if not matching_project:
            logger.warning("No matching project found with given project_code and fin_code")
            return jsonify({'error': 'No matching project found with given project_code and fin_code'}), 400

        new_subject = SubjectOfPurchase(
            project_code=data['project_code'],
            equipment_name=data['equipment_name'],
            unit_of_measure=data['unit_of_measure'],
            price=data['price'],
            quantity=data['quantity'],
            total_amount=data['price'] * data['quantity']
        )
        db.session.add(new_subject)
        db.session.commit()
        return jsonify({'message': 'Subject added successfully'}), 201

    except Exception as e:
        logger.error(f"Error while adding subject: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# @subject_bp.route('/api/get-subjects', methods=['GET'])
# def get_subjects():
#     try:
        
#         results = db.session.query(SubjectOfPurchase).join(
#             Project,
#             (SubjectOfPurchase.project_code == Project.project_code) &
#             (SubjectOfPurchase.fin_code == Project.fin_kod)
#         ).all()

#         response = [{
#             'project_code': s.project_code,
#             'fin_code': s.fin_code,
#             'equipment_name': s.equipment_name,
#             'unit_of_measure': s.unit_of_measure,
#             'price': s.price,
#             'quantity': s.quantity,
#             'total_amount': s.total_amount
#         } for s in results]

#         return jsonify(response), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 400


@subject_bp.route("/api/subject/smeta/<int:project_code>", methods=['GET'])
@token_required([0, 1])
def get_subject_smeta_by_project_code(project_code):
    try:
        subject_smeta = SubjectOfPurchase.query.filter_by(project_code=project_code).all()

        return handle_success([subject.subject_details() for subject in subject_smeta], "Smeta fetched successfully.")
    
    except Exception as e:
        return handle_global_exception(str(e))
    
@subject_bp.route('/api/update-subject/<int:project_code>', methods=['PATCH'])
@token_required([0])
def update_subject(project_code):
    data = request.get_json()

    try:
        subject = SubjectOfPurchase.query.filter_by(project_code=project_code).first()

        if not subject:
            return jsonify({'error': 'Subject not found with the provided project_code'}), 404

        if 'equipment_name' in data:
            subject.equipment_name = data['equipment_name']
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



@subject_bp.route('/api/delete/smeta/subject/<int:id>', methods=['DELETE'])
@token_required([0])
def delete_subject(id):
    try:
        subject = SubjectOfPurchase.query.filter_by(id=id).first()

        if not subject:
            return jsonify({'error': 'Subject not found with the provided project_code'}), 404

        db.session.delete(subject)
        db.session.commit()
        return jsonify({'message': 'Subject deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400