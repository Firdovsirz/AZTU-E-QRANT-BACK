import os
from flask import Flask
from flask_cors import CORS
from config.config import Config 
from extentions.db import migrate, db
from controllers.AuthController import auth_bp
from controllers.UserController import user_bp
from controllers.ProjectController import project_offer
from controllers.CollaboratorController import collaborator_bp
from controllers.smetaControllers.rentController import rent_bp
from controllers.smetaControllers.smetaCotroller import smeta_bp
from controllers.smetaControllers.salaryController import salary_bp
from controllers.smetaControllers.subjectController import subject_bp
from controllers.smetaControllers.other_expensesController import other_exp
from controllers.smetaControllers.servicesTableController import services_bp

def main_app():
    app = Flask(__name__)
    app.config.from_object(Config)


    CORS(
        app,
        origins=["http://localhost:5173"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Content-Disposition"],
        methods=["GET", "POST", "OPTIONS", "DELETE"]
    )

    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(rent_bp)
    app.register_blueprint(smeta_bp)
    app.register_blueprint(salary_bp)
    app.register_blueprint(other_exp)
    app.register_blueprint(subject_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(project_offer)
    app.register_blueprint(collaborator_bp)

    return app

if __name__ == '__main__':
    app = main_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
