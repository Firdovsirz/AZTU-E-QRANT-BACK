from models.authModel import Auth
from flask_cors import cross_origin
from flask import Blueprint, request
from models.userModel import db, User
from utils.jwt_util import encode_auth_token
from exceptions.exception import handle_creation
from exceptions.exception import handle_conflict
from exceptions.exception import handle_not_found
from exceptions.exception import handle_unauthorized
from exceptions.exception import handle_missing_field
from exceptions.exception import handle_signin_success

auth_bp = Blueprint('auth', __name__)
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@auth_bp.route('/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        logger.info("Signup request data: %s", data)

        required_fields = ['fin_kod', 'password', "role"]

        for field in required_fields:
            if field not in data:
                logger.warning("Missing field in request data: %s", field)
                return handle_missing_field(404)

        fin_kod = data.get('fin_kod')
        password = data.get('password')
        role = data.get('role')

        logger.info("Checking if user already exists: fin_kod=%s", fin_kod)
        if Auth.query.filter_by(fin_kod=fin_kod).first() or User.query.filter_by(fin_kod=fin_kod).first():
            logger.warning("User already exists with fin_kod: %s", fin_kod)
            return handle_conflict(409)

        auth_record = Auth(fin_kod=fin_kod)
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
    data = request.get_json()
    fin_kod = data.get('fin_kod')
    password = data.get('password')

    auth_data = Auth.query.filter_by(fin_kod=fin_kod).first()
    user_data = User.query.filter_by(fin_kod=fin_kod).first()

    if not auth_data or not auth_data.check_password(password):
        return handle_unauthorized(401, "Invalid credentials.")
    
    token = encode_auth_token(auth_data.id, fin_kod, user_data.profile_completed)

    return handle_signin_success(fin_kod, "Signed in successfully.", token)