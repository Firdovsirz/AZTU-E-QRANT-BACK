import random
from extentions.db import db
from datetime import datetime
from models.authModel import Auth
from models.userModel import User
from flask_cors import cross_origin
from models.projectModel import Project
from utils.decarator import role_required
from flask import Blueprint, request, current_app
from exceptions.exception import handle_missing_field, handle_conflict, handle_creation, handle_specific_not_found, handle_success, handle_global_exception

project_offer = Blueprint('project_offer', __name__)

def generate_unique_project_code():
    while True:
        code = random.randint(10000000, 99999999) 
        if not Project.query.filter_by(project_code=code).first():
            return code


@project_offer.route('/api/save/project', methods=['POST'])
@cross_origin()
def save_project():
    current_app.logger.info("POST /api/save/project called")
    data = request.get_json()
    current_app.logger.info(f"Received data: {data}")
    fin_kod = data.get('fin_kod')

    if not fin_kod:
        current_app.logger.warning("Missing fin_kod in request")
        return handle_missing_field(404)

    project = Project.query.filter_by(fin_kod=fin_kod).first()
    if not project:
        current_app.logger.info(f"No existing project found for fin_kod={fin_kod}, creating new one.")
        project = Project(
            fin_kod=fin_kod,
            project_code=generate_unique_project_code()
        )
        db.session.add(project)
    else:
        current_app.logger.info(f"Updating existing project with fin_kod={fin_kod}")

    for field in [
        'project_name', 'project_purpose', 'project_annotation',
        'project_key_words', 'project_scientific_idea', 'project_structure',
        'team_characterization', 'project_monitoring', 'project_requirements',
        'project_assessment'
    ]:
        if field in data:
            setattr(project, field, data[field])

    if 'project_deadline' in data:
        try:
            project.project_deadline = datetime.strptime(data['project_deadline'], '%Y-%m-%d')
        except ValueError:
            return {'error': 'Invalid date format. Use YYYY-MM-DD.'}, 400

    required_fields = [
        'project_name', 'project_purpose', 'project_annotation',
        'project_key_words', 'project_scientific_idea', 'project_structure',
        'team_characterization', 'project_monitoring', 'project_requirements',
        'project_deadline'
    ]

    all_fields_filled = all(getattr(project, field) for field in required_fields)

    project.approved = 1 if all_fields_filled else 0
    current_app.logger.info(f"Project approved={project.approved}")

    db.session.commit()

    if project.approved == 1:
        current_app.logger.info("Project fully submitted and approved=1.")
        return {'message': 'Project fully submitted and approved=1.'}, 200
    else:
        current_app.logger.info("Project draft saved with approved=0.")
        return {'message': 'Project draft saved with approved=0.'}, 200
    
def serialize_project(project):
    return {
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
        'project_deadline': project.project_deadline.strftime('%Y-%m-%d') if project.project_deadline else None,
        'approved': project.approved
    }

@project_offer.route("/api/approve_project", methods=['POST'])
def approve_project():
    try:
        project_details = request.get_json()

        fin_kod = project_details.get('fin_kod')
        project_code = project_details.get('project_code')

        user = Auth.query.filter_by(fin_kod=fin_kod).first()

        if not user:
            return handle_specific_not_found('User not found.')
        
        project = Project.query.filter_by(project_code=project_code,  fin_kod=fin_kod).first()

        if not project:
            return handle_specific_not_found('Project not found.')
        
        profile_approved = User.query.filter_by(fin_kod=fin_kod).first().profile_completed

        if not profile_approved:
            return {'error': 'User profile is not completed.', 'status': 403}, 403

        project.approved = 1
        db.session.commit()

        return {'message': 'Project approved successfully.'}, 200
    
    except Exception as e:
        return handle_global_exception(str(e))
        

@project_offer.route('/api/projects', methods=['GET'])
@cross_origin()
def get_projects():
    # approved_param = request.args.get('approved')

    # if approved_param is None:
    #     return {'error': 'approved parameter is required (0 or 1).'}, 400

    # try:
    #     approved = int(approved_param)
    #     if approved not in [0, 1]:
    #         raise ValueError
    # except ValueError:
    #     return {'error': 'approved must be 0 or 1.'}, 400

    # projects = Project.query.filter_by(approved=approved).all()
    # return {
    #     'projects': [serialize_project(p) for p in projects],
    #     'approved': approved
    # }, 200
    try:
        project_list = []
        projects = Project.query.all()

        if not projects:
            return handle_specific_not_found('No project found.')

        for project in projects:
            project_data = project.project_detail()

            fin_kod = project_data.get('fin_kod')
            user = User.query.filter_by(fin_kod=fin_kod).first()

            if user:
                project_data['user'] = {
                    'name': user.name,
                    'surname': user.surname
                }
            else:
                project_data['user'] = None

            project_list.append(project_data)

        return handle_success(project_list, 'Projects fetched successfully.')
    except Exception as e:
        return handle_global_exception(str(e))
    
@project_offer.route("/api/project/<string:fin_kod>")
def get_project_by_fin_kod(fin_kod):
    try:
        user = Auth.query.filter_by(fin_kod=fin_kod).first()

        if not user:
            return handle_specific_not_found('User not found.')
        
        project = Project.query.filter_by(fin_kod=fin_kod).first()

        return handle_success(project.project_detail(), 'Project fetched successfully')
    except Exception as e:
        return handle_global_exception(str(e))

# @project_offer.route('/api/projects/approved', methods=['GET'])
# @cross_origin()
# def get_approved_projects():
#     projects = Project.query.filter_by(approved=1).all()
#     return {'approved_projects': [serialize_project(p) for p in projects]}, 200


# @project_offer.route('/api/projects/pending', methods=['GET'])
# @cross_origin()
# def get_pending_projects():
#     projects = Project.query.filter_by(approved=0).all()
#     return {'pending_projects': [serialize_project(p) for p in projects]}, 200

# def serialize_project(project):
#     return {
#         'project_code': project.project_code,
#         'fin_kod': project.fin_kod,
#         'project_name': project.project_name,
#         'project_purpose': project.project_purpose,
#         'project_annotation': project.project_annotation,
#         'project_key_words': project.project_key_words,
#         'project_scientific_idea': project.project_scientific_idea,
#         'project_structure': project.project_structure,
#         'team_characterization': project.team_characterization,
#         'project_monitoring': project.project_monitoring,
#         'project_requirements': project.project_requirements,
#         'project_assessment': project.project_assessment,
#         'project_deadline': project.project_deadline.strftime('%Y-%m-%d') if project.project_deadline else None,
#         'approved': project.approved
#     }



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
#@role_required([1])
def delete_project_offer():
    data = request.get_json()
    fin_kod = data.get('fin_kod')

    if not fin_kod:
        return {'error': 'fin_kod parameter is required.'}, 400

    project = Project.query.filter_by(fin_kod=fin_kod).first()

    if not project:
        return {'error': 'Project not found for the provided fin_kod.'}, 404

    # Approved olanların silinmemesi ucun, isteye gore bunu acariq
    # if project.approved == 1:
    #     return {'error': 'Approved projects cannot be deleted.'}, 403

    db.session.delete(project)
    db.session.commit()

    return {'message': 'Project successfully deleted.'}, 200
