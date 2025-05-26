# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_db_name.db'

# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

# import modelshow


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate(db)