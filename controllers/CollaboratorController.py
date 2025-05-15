from extentions.db import db
from models.userModel import User
from models.authModel import Auth
from flask_cors import cross_origin
from flask import Blueprint, request
from models.projectModel import Project
from utils.decarator import role_required
from models.collaboratorModel import Collaborator
from exceptions.exception import handle_not_found
from exceptions.exception import handle_global_exception
from exceptions.exception import handle_specific_not_found
from exceptions.exception import handle_missing_field, handle_conflict, handle_creation, handle_success

collaborator_bp = Blueprint('collaborator_bp', __name__)

@collaborator_bp.route("/api/collaborators", methods=['GET'])
def get_collaborators():
    try:
        collaborator_list = []
        collaborators = Collaborator.query.all()
        if not collaborators:
            return handle_not_found(404)
        for collaborator in collaborators:
            collaborator_list.append(collaborator)
        print(collaborator_list)
    except Exception as e:
        return handle_global_exception(str(e))

@collaborator_bp.route("/api/collaborators/<int:project_code>")
def get_collaborators_by_fin_kod(project_code):
    try:
        collaborator_list = []
        collborators = Collaborator.query.filter_by(project_code=project_code).all()
        if not collborators:
            return handle_specific_not_found('No collaborator found.')

        for collaborator in collborators:
            user = User.query.filter_by(fin_kod=collaborator.fin_kod).first()
            if user:
                collaborator_list.append({
                    'fin_kod': collaborator.fin_kod,
                    'project_code': collaborator.project_code,
                    'name': user.name,
                    'surname': user.surname,
                    'image': user.get_user_image()
                })

        return {'data': collaborator_list, 'status': 200}, 200
    
    except Exception as e:
        return handle_global_exception(str(e))

@collaborator_bp.route('/api/be-collaborator', methods=['POST'])
def be_collaborator():
    try:
        collaborator_details = request.get_json()
        required_fields = ['fin_kod', 'project_code']

        for field in required_fields:
            if field not in collaborator_details:
                return handle_missing_field(404)
            
        fin_kod = collaborator_details.get('fin_kod')
        project_code = collaborator_details.get('project_code')
        
        user = Auth.query.filter_by(fin_kod=fin_kod).first()
        project = Project.query.filter_by(project_code=project_code).first()

        if not user:
            handle_specific_not_found("User not found.")
        if not project:
            handle_specific_not_found("Project not found.")

        profile_approved = User.query.filter_by(fin_kod=fin_kod).first().profile_completed

        if not profile_approved:
            return {'error': 'User profile is not completed.', 'status': 403}, 403
        
        new_collaborator_record = Collaborator(
            project_code=project_code,
            fin_kod=fin_kod
        )

        db.session.add(new_collaborator_record) 
        db.session.commit()

        return handle_creation("Collaborator added successfully.")

    except Exception as e:
        return handle_global_exception(str(e))