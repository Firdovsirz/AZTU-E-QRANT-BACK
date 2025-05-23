from models.authModel import Auth
from flask_cors import cross_origin
from flask import Blueprint, request
from models.userModel import db, User
from models.projectModel import  Project
from utils.jwt_util import encode_auth_token
from exceptions.exception import handle_creation
from exceptions.exception import handle_conflict
from exceptions.exception import handle_not_found
from models.collaboratorModel import  Collaborator
from exceptions.exception import handle_unauthorized
from exceptions.exception import handle_missing_field
from exceptions.exception import handle_signin_success

auth_bp = Blueprint('auth', __name__)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        logger.info("Signup request data: %s", data)

        required_fields = ['fin_kod', 'password', 'user_type', 'academic_type', 'project_role']

        for field in required_fields:
            if field not in data:
                logger.warning("Missing field in request data: %s", field)
                return handle_missing_field(404)

        fin_kod = data.get('fin_kod')
        password = data.get('password')
        user_type = data.get('user_type')
        academic_type = data.get('academic_type')
        project_role = data.get('project_role')

        logger.info("Checking if user already exists: fin_kod=%s", fin_kod)
        if Auth.query.filter_by(fin_kod=fin_kod).first() or User.query.filter_by(fin_kod=fin_kod).first():
            logger.warning("User already exists with fin_kod: %s", fin_kod)
            return handle_conflict(409)

        auth_record = Auth(
            fin_kod=fin_kod,
            user_type=user_type,
            academic_role=academic_type,
            project_role=project_role
        )
        auth_record.set_password(password)

        user_record = User(
            fin_kod=fin_kod,
            profile_completed=0,
        )

        logger.info("Adding new user and auth records to database")
        db.session.add(auth_record)
        db.session.add(user_record)
        db.session.commit()

        logger.info("User successfully registered")
        return handle_creation("User registered successfully.")

    except Exception as e:
        logger.exception("An unexpected error occurred during signup")
        return {"error": "Internal server error", "message": str(e)}, 500

@auth_bp.route('/auth/signin', methods=['POST'])
@cross_origin(origins=["http://localhost:5173"], supports_credentials=True)
def signin():
    try:
        data = request.get_json()
        fin_kod = data.get('fin_kod')
        password = data.get('password')
        user_type = data.get('user_type')
        academic_type = data.get('academic_type')

        if not all([fin_kod, password, user_type is not None, academic_type is not None]):
            logger.warning("Missing required fields in request")
            return handle_missing_field(404)

        logger.info("Attempting signin for FIN: %s", fin_kod)

        auth_data = Auth.query.filter_by(fin_kod=fin_kod).first()
        if auth_data is None:
            logger.warning("No auth record found for FIN: %s", fin_kod)
            return handle_unauthorized(401, "Invalid FIN code or user not found.")

        if not auth_data.check_password(password):
            logger.warning("Invalid password for FIN: %s", fin_kod)
            return handle_unauthorized(401, "Incorrect password.")

        if str(auth_data.user_type) != str(user_type):
            logger.warning("User type mismatch for FIN: %s. Expected %s, got %s", fin_kod, auth_data.user_type, user_type)
            return handle_unauthorized(401, "User type does not match.")

        if str(auth_data.academic_role) != str(academic_type):
            logger.warning("Academic role mismatch for FIN: %s. Expected %s, got %s", fin_kod, auth_data.academic_role, academic_type)
            return handle_unauthorized(401, "Academic role does not match.")

        user_data = User.query.filter_by(fin_kod=fin_kod).first()
        profile_completed = user_data.profile_completed
        if user_data is None:
            logger.warning("No user record found for FIN: %s", fin_kod)
            return handle_unauthorized(401, "User data not found.")
        
        project_role = auth_data.project_role
        
        if project_role == 0:
            project_owner = Project.query.filter_by(fin_kod=fin_kod).first()
            project_code = project_owner.project_code if project_owner else None

        
        if project_role == 1:
            collaborator = Collaborator.query.filter_by(fin_kod=fin_kod).first()
            project_code = collaborator.project_code if collaborator else None

        signin_data = {
            "auth": auth_data.auth_details(),
            "project_code": project_code,
            "profile_completed": profile_completed
        }

        token = encode_auth_token(auth_data.id, fin_kod, user_data.profile_completed)
        logger.info("User signed in successfully: %s", fin_kod)
        return handle_signin_success(signin_data, "Signed in successfully.", token)

    except Exception as e:
        logger.exception("Unexpected error during signin")
        return {"error": "Internal server error", "message": str(e)}, 500