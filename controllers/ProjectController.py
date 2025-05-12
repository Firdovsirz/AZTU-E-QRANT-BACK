import random
from extentions.db import db
from datetime import datetime
from models.userModel import User
from flask_cors import cross_origin
from flask import Blueprint, request
from models.projectModel import Project
from utils.decarator import role_required
from exceptions.exception import handle_missing_field, handle_conflict, handle_creation

project_offer = Blueprint('project_offer', __name__)

def generate_unique_project_code():
    while True:
        code = random.randint(10000000, 99999999) 
        if not Project.query.filter_by(project_code=code).first():
            return code

@project_offer.route('/api/create/project', methods=['POST'])
@role_required([1])
@cross_origin()
def create_project_offer():
    data = request.get_json()

    required_fields = [
        'fin_kod', 'project_name', 'project_purpose', 'project_annotation',
        'project_key_words', 'project_scientific_idea', 'project_structure', 'team_characterization',
        'project_monitoring', 'project_requirements', 'project_deadline'
    ]

    for field in required_fields:
        if field not in data:
            return handle_missing_field(404)

    fin_kod = data.get('fin_kod')

    if not User.query.filter_by(fin_kod=fin_kod).first():
        return handle_conflict(409)

    if Project.query.filter_by(fin_kod=fin_kod).first():
        return handle_conflict(409)

    try:
        project_deadline = datetime.strptime(data.get('project_deadline'), '%Y-%m-%d')
    except ValueError:
        return {'error': 'Invalid date format. Use YYYY-MM-DD.'}, 400

    project_code = generate_unique_project_code()

    new_project = Project(
        project_code=project_code,
        fin_kod=fin_kod,
        project_name=data.get('project_name'),
        project_purpose=data.get('project_purpose'),
        project_annotation=data.get('project_annotation'),
        project_key_words=data.get('project_key_words'),
        project_scientific_idea=data.get('project_scientific_idea'),
        project_structure=data.get('project_structure'),
        team_characterization=data.get('team_characterization'),
        project_monitoring=data.get('project_monitoring'),
        project_requirements=data.get('project_requirements'),
        project_assessment=data.get('project_assessment', ''),
        project_deadline=project_deadline
    )

    db.session.add(new_project)
    db.session.commit()

    return handle_creation("Project offer successfully submitted.")


@project_offer.route('/api/projects', methods=['GET'])
@role_required([0, 1])
@cross_origin()
def get_project_offer():
    fin_kod = request.args.get('fin_kod')

    if not fin_kod:
        return {'error': 'fin_kod parameter is required.'}, 400

    project = Project.query.filter_by(fin_kod=fin_kod).first()

    if not project:
        return {'error': 'Project not found for the provided fin_kod.'}, 404

    project_data = {
        'project_code': project.project_code,
        'fin_kod': project.fin_kod,
        'project_name': project.project_name,
        'project_purpose': project.project_purpose,
        'project_annotation': project.project_annotation,
        'project_key_words': project.project_key_words,
        'project_scientific_idea': project.project_scientific_idea,
        'project_structure': project.project_structure,
        'team_characterization': project.team_characterization,
        'project_monitoring': project.project_monitoring,
        'project_requirements': project.project_requirements,
        'project_assessment': project.project_assessment,
        'project_deadline': project.project_deadline.strftime('%Y-%m-%d')
    }

    return {'project': project_data}, 200


@project_offer.route('/api/upd/project', methods=['PATCH'])
@cross_origin()
def update_project_offer():
    data = request.get_json()

    fin_kod = data.get('fin_kod')
    if not fin_kod:
        return {'error': 'fin_kod field is required to update a project.'}, 400

    project = Project.query.filter_by(fin_kod=fin_kod).first()
    if not project:
        return {'error': 'Project not found for the provided fin_kod.'}, 404

    
    updatable_fields = [
        'project_name', 'project_purpose', 'project_annotation',
        'project_key_words', 'project_scientific_idea', 'project_structure',
        'team_characterization', 'project_monitoring', 'project_requirements',
        'project_assessment', 'project_deadline'
    ]

    for field in updatable_fields:
        if field in data:
            if field == 'project_deadline':
                try:
                    setattr(project, field, datetime.strptime(data[field], '%Y-%m-%d'))
                except ValueError:
                    return {'error': 'Invalid date format for project_deadline. Use YYYY-MM-DD.'}, 400
            else:
                setattr(project, field, data[field])

    db.session.commit()

    return {'message': 'Project successfully updated.'}, 200



@project_offer.route('/api/delete/project', methods=['DELETE'])
@cross_origin()
def delete_project_offer():
    fin_kod = request.args.get('fin_kod')

    if not fin_kod:
        return {'error': 'fin_kod parameter is required.'}, 400

    project = Project.query.filter_by(fin_kod=fin_kod).first()

    if not project:
        return {'error': 'Project not found for the provided fin_kod.'}, 404

    db.session.delete(project)
    db.session.commit()

    return {'message': 'Project successfully deleted.'}, 200