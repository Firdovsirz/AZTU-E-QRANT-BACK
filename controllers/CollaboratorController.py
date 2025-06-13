import logging
from extentions.db import db
from models.userModel import User
from models.authModel import Auth
from flask_cors import cross_origin
from flask import Blueprint, request
from models.projectModel import Project
from utils.decarator import role_required
from utils.jwt_required import token_required
from models.collaboratorModel import Collaborator
from exceptions.exception import handle_not_found
from exceptions.exception import handle_global_exception
from exceptions.exception import handle_specific_not_found
from exceptions.exception import handle_missing_field, handle_creation, handle_success

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

collaborator_bp = Blueprint('collaborator_bp', __name__)

@collaborator_bp.route("/api/collaborators", methods=['GET'])
@token_required([1])
def get_collaborators():
    try:
        logger.debug("Fetching all collaborators")
        collaborator_list = []
        collaborators = Collaborator.query.all()
        if not collaborators:
            return handle_not_found(404)
        for collaborator in collaborators:
            collaborator_list.append(collaborator)
        logger.debug(f"Collaborator list: {collaborator_list}")
    except Exception as e:
        return handle_global_exception(str(e))

@collaborator_bp.route("/api/collaborators/<int:project_code>")
@token_required([1])
def get_collaborators_by_fin_kod(project_code):
    try:
        logger.debug(f"Fetching collaborators for project code: {project_code}")
        collaborator_list = []
        collborators = Collaborator.query.filter_by(project_code=project_code).all()
        if not collborators:
            logger.debug("No collaborators found for the given project code.")
            return handle_specific_not_found('No collaborator found.')

        for collaborator in collborators:
            user = User.query.filter_by(fin_kod=collaborator.fin_kod).first()
            user_role = Auth.query.filter_by(fin_kod=collaborator.fin_kod).first().project_role

            if user:
                logger.debug(f"Adding collaborator to response: fin_kod={collaborator.fin_kod}, name={user.name}, surname={user.surname}, role={user_role}")
                collaborator_list.append({
                    'fin_kod': collaborator.fin_kod,
                    'project_code': collaborator.project_code,
                    'name': user.name,
                    'surname': user.surname,
                    'father_name': user.father_name,
                    'image': user.get_user_image(),
                    'project_role': user_role
                })

        return {'data': collaborator_list, 'status': 200}, 200
    
    except Exception as e:
        return handle_global_exception(str(e))
    
@collaborator_bp.route("/api/project/owner/<int:project_code>", methods=['GET'])
@token_required([1])
def get_project_owner(project_code):
    try:
        logger.debug(f"Fetching project owner for project code: {project_code}")

        owner_fin_kod = Project.query.filter_by(project_code=project_code).first().fin_kod
        logger.debug(f"Project owner fin_kod: {owner_fin_kod}")

        user = User.query.filter_by(fin_kod=owner_fin_kod).first()
        logger.debug(f"Owner found: name={user.name}, surname={user.surname}")

        if not user:
            return handle_specific_not_found("Owner not found.")
        
        owner_details = {
            'name': user.name,
            'surname': user.surname,
            'father_name': user.father_name,
        }

        return handle_success(owner_details, 'Owner fetched successfully.')

    except Exception as e:
        return handle_global_exception(str(e))

@collaborator_bp.route('/api/be-collaborator', methods=['POST'])
@token_required([1])
def be_collaborator():
    try:
        logger.debug("Received request to become collaborator")
        collaborator_details = request.get_json()
        required_fields = ['fin_kod', 'project_code']

        for field in required_fields:
            if field not in collaborator_details:
                return handle_missing_field(404)
            
        fin_kod = collaborator_details.get('fin_kod')
        project_code = collaborator_details.get('project_code')
        
        logger.debug(f"fin_kod: {fin_kod}, project_code: {project_code}")

        user = Auth.query.filter_by(fin_kod=fin_kod).first()
        project = Project.query.filter_by(project_code=project_code).first()

        if not user:
            logger.debug("User not found.")
            return handle_specific_not_found("User not found.")
        if not project:
            logger.debug("Project not found.")
            return handle_specific_not_found("Project not found.")

        profile_approved = User.query.filter_by(fin_kod=fin_kod).first().profile_completed

        if not profile_approved:
            logger.debug("User profile not completed.")
            return {'error': 'User profile is not completed.', 'status': 403}, 403
        
        new_collaborator_record = Collaborator(
            project_code=project_code,
            fin_kod=fin_kod
        )

        logger.debug("Adding new collaborator to the database")
        db.session.add(new_collaborator_record) 
        db.session.commit()

        return handle_creation("Collaborator added successfully.")

    except Exception as e:
        logger.exception("An error occurred while processing be-collaborator request")
        return handle_global_exception(str(e))