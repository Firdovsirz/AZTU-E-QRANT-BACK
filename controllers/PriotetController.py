from extentions.db import db
from datetime import datetime
from flask import Blueprint, request
from models.prioritetModel import Priotet
from utils.jwt_required import token_required
from exceptions.exception import handle_missing_field, handle_specific_not_found, handle_success, handle_global_exception, handle_creation

priotet_bp = Blueprint('priotet', __name__)

@priotet_bp.route('/api/create-priotet', methods=['POST'])
@token_required([0, 1, 2])
def create_priotet():
    try:
        data = request.get_json()
        prioritet_name = data.get("prioritet_name")
        prioritet_code = data.get("prioritet_code")

        if not prioritet_name or not prioritet_code:
            return handle_missing_field()

        new_prioritet = Priotet(
            prioritet_name=prioritet_name,
            prioritet_code=prioritet_code,
            created_at=datetime.utcnow()
        )
        db.session.add(new_prioritet)
        db.session.commit()

        return handle_creation("Prioritet successfully created")

    except Exception as e:
        return handle_global_exception(e)


@priotet_bp.route('/api/priotets', methods=['GET'])
@token_required([0, 1, 2])
def get_priotets():
    try:
        prioritets = Priotet.query.all()

        data = [
            {
                "id": p.id,
                "prioritet_name": p.prioritet_name,
                "prioritet_code": p.prioritet_code,
                "created_at": p.created_at.isoformat() if p.created_at else None
            }
            for p in prioritets
        ]
        return handle_success(data, "Priotets fetched successfully")
    except Exception as e:
        return handle_global_exception(e)
    