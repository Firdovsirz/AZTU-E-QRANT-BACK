import os
import jwt
import datetime
from functools import wraps
from models.userModel import User
from flask import current_app, request, jsonify


SECRET_KEY = os.getenv('SECRET_KEY')

def encode_auth_token(user_id, fin_kod, profile_completed, role):
    try:
        user = User.query.filter_by(fin_kod=fin_kod).first()
        if not user:
            raise ValueError("User not found")

        expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)

        payload = {
            'sub': str(user_id),
            'fin_kod': str(fin_kod),
            'profile_completed': profile_completed,
        	'role': role,
            'exp': expiration_time
        }

        auth_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return auth_token

    except Exception as e:
        current_app.logger.error(f"Error encoding token: {e}")
        return str(e)


def decode_auth_token(auth_token):
    try:
        current_app.logger.debug(f"Decoding token: {auth_token}")

        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=['HS256'], options={"require": ["exp"]})

        current_app.logger.debug(f"Decoded payload: {payload}")

        return {
            'user_id': payload['sub'],
            'fin_kod': payload['fin_kod'],
            'profile_completed': payload['profile_completed'],
        	'role': payload['role']
        }

    except jwt.ExpiredSignatureError:
        current_app.logger.warning("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        current_app.logger.warning(f"Invalid token: {e}")
        return None
    except Exception as e:
        current_app.logger.error(f"Error decoding token: {e}")
        return None