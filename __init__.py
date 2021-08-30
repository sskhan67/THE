"""Initialize app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import config

db = SQLAlchemy()
login_manager = LoginManager()
create_admin_user = True

def create_app():
    """Construct the core app object."""
    app = Flask(__name__)

    # Application Configuration
    app.config.from_object(config.Config)

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        import auth
        import role
        import companies

        # Register Blueprints
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(role.role_bp)
        app.register_blueprint(companies.company_bp)

        #uncomment the below line to reset the database
        #db.drop_all()
        # Create Database Models
        db.create_all()

        return app

