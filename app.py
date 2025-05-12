from flask import Flask
from flask_cors import CORS
from extentions.db import db
from config.config import Config
from controllers.AuthController import auth_bp
from controllers.UserController import user_bp
from controllers.ProjectController import project_offer

def main_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        origins=["http://localhost:5173"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization", "Content-Disposition"],
        methods=["GET", "POST", "OPTIONS"]
    )

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(project_offer)

    return app

if __name__ == '__main__':
    app = main_app()
    app.run(host="0.0.0.0", port=5000)