import random
from extentions.db import db
from datetime import datetime
from models.authModel import Auth
from models.userModel import User
from config.limiter import limiter
from models.projectModel import Project
from utils.jwt_required import token_required
from models.smetaModels.smetaModel import Smeta
from models.collaboratorModel import Collaborator
from flask import Blueprint, request, current_app
from models.collaboratorModel import Collaborator
from models.smetaModels.salaryModel import Salary
from exceptions.exception import handle_missing_field, handle_specific_not_found, handle_success, handle_global_exception

project_offer = Blueprint('project_offer', __name__)

def generate_unique_project_code():
    while True:
        code = random.randint(10000000, 99999999) 
        if not Project.query.filter_by(project_code=code).first():
            return code


@project_offer.route('/api/save/project', methods=['POST'])
@limiter.limit("100 per second")
@token_required([0, 2])
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
        'project_assessment', 'collaborator_limit', 'max_smeta_amount', 'priotet'
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
        'project_deadline', 'collaborator_limit', 'max_smeta_amount', 'priotet'
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
@limiter.limit("100 per second")
@token_required([0, 2])
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
@limiter.limit("100 per second")
@token_required([0, 1, 2])
def get_projects():
    current_app.logger.info("GET /api/projects called")
    try:
        project_list = []
        projects = Project.query.all()

        if not projects:
            current_app.logger.warning("No projects found in database")
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

        current_app.logger.info(f"Returning {len(project_list)} projects")
        return handle_success(project_list, 'Projects fetched successfully.')
    except Exception as e:
        current_app.logger.error(f"Exception in /api/projects: {e}", exc_info=True)
        return handle_global_exception(str(e))
    
@project_offer.route("/api/project/<string:fin_kod>")
@limiter.limit("100 per second")
@token_required([0 ,1, 2])
def get_project_by_fin_kod(fin_kod):
    try:
        user = Auth.query.filter_by(fin_kod=fin_kod).first()

        if not user:
            return handle_specific_not_found('User not found.')
        
        project = Project.query.filter_by(fin_kod=fin_kod).first()

        return handle_success(project.project_detail(), 'Project fetched successfully')
    except Exception as e:
        return handle_global_exception(str(e))
    
@project_offer.route("/api/project/<int:project_code>", methods=['GET'])
@limiter.limit("100 per second")
@token_required([0, 1, 2])
def project_by_project_code(project_code):

    try:
        
        project = Project.query.filter_by(project_code=project_code).first()

        if not project:
            return handle_specific_not_found("Project not found.")
        
        return handle_success(project.project_detail(), "Project data fetched succesfully.")
    
    except Exception as e:
        return handle_global_exception(str(e))

@project_offer.route('/api/upd/project', methods=['PATCH'])
@limiter.limit("100 per second")
@token_required([0, 2])
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
        'project_assessment', 'project_deadline', 'collaborator_limit', 'max_smeta_amount'
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
@limiter.limit("100 per second")
@token_required([0, 2])
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

@project_offer.route("/api/project-details/<int:project_code>", methods=['GET'])
@limiter.limit("100 per second")
@token_required([0, 1, 2])
def get_project_details_by_project_code(project_code):

    try:
        
        project = Project.query.filter_by(project_code=project_code).first()

        if not project:
            return handle_specific_not_found("Project not found for the project code.")
        
        project_owner_fin_kod = project.fin_kod

        project_owner = User.query.filter_by(fin_kod=project_owner_fin_kod).first()

        collaborator_list = []

        collaborators = Collaborator.query.filter_by(project_code=project_code).all()

        for collaborator in collaborators:

            collaborator_details = User.query.filter_by(fin_kod=collaborator.fin_kod).first()

            collaborator_data = {
                "name": collaborator_details.name,
                "surname": collaborator_details.surname,
                "father_name": collaborator_details.father_name,
                "fin_kod": collaborator_details.fin_kod,
                "image": collaborator_details.get_user_image()
            }

            collaborator_list.append(collaborator_data)

        project_smeta_salary_list = []

        preoject_smeta_salaries = Salary.query.filter_by(project_code=project_code).all()

        for salary_smeta in preoject_smeta_salaries:

            project_smeta_salary_list.append(salary_smeta.salary_details())
        
        project_data = {
            "project_owner": {
                "name": project_owner.name,
                "surname": project_owner.surname,
                "father_name": project_owner.father_name,
                "fin_kod": project_owner_fin_kod
            },
            "collaborators": collaborator_list,
            "project_details": project.project_detail(),
            "project_saalry_smeta": project_smeta_salary_list
        }
        
        return handle_success(project_data, "Project data fetched successfully")
    
    except Exception as e:
        return handle_global_exception(str(e))


@project_offer.route("/api/submit-project", methods=['POST'])
@limiter.limit("100 per second")
@token_required([0, 2])
def submit_project():
    data = request.get_json()
    project_code = data.get('project_code')

    if not project_code:
        return {'error': 'project_code field is required.'}, 400

    project = Project.query.filter_by(project_code=project_code).first()

    if not project:
        return {'error': 'Project not found for the provided project_code.'}, 404
    smeta = Smeta.query.filter_by(project_code=project_code).first()

    total_amount = sum([
        smeta.total_fee,
        smeta.total_salary,
        smeta.defense_fund,
        smeta.total_equipment,
        smeta.total_services,
        smeta.total_rent,
        smeta.other_expenses
    ])

    if total_amount > 30000:
        return {
            "status": 409,
            "message": "Total amount is over 30000"
        }, 409

    project.submitted = True
    project.submitted_at = datetime.utcnow()

    db.session.commit()

    return {'message': 'Project successfully submitted.'}, 200

@project_offer.route("/api/col-project/<string:fin_kod>")
@limiter.limit("100 per second")
@token_required([1])
def collaborator_projet(fin_kod):
    collaborator = Collaborator.query.filter_by(fin_kod=fin_kod).first()
    
    if not collaborator:
        return {'error': 'Collaborator not found'}, 404
    
    return {
        'status': 200,
        'message': "Project code fetched successfully.",
        'project_code': collaborator.project_code,
    }, 200

@project_offer.route("/api/project-owner/<int:project_code>")
@limiter.limit("100 per second")
def get_project_owner(project_code):
    project = Project.query.filter_by(project_code=project_code).first()
    
    if not project:
        return {
            "status": 404,
            "message": "Project not found."
        }, 404

    owner_fin_kod = project.fin_kod
    owner = User.query.filter_by(fin_kod=owner_fin_kod).first()

    if not owner:
        return {
            "status": 404,
            "message": "No user found."
        }, 404
    
    return {
        "status": 200,
        "message": "Owner fetched successfully.",
        "owner_data": {
            "name": owner.name,
            "surname": owner.surname,
            "father_name": owner.father_name,
            "fin_kod": owner.fin_kod,
            "project_role": owner.work_location,
            "image": owner.get_user_image()
        }
    }, 200