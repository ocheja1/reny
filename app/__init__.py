from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
DB_NAME = "rently_web.db"  # Change the database name as needed


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(32)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://rently_admin:rently@localhost/rently_web'  # MySQL URI
    db.init_app(app)

    # Import and register blueprints
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    with app.app_context():
        db.create_all()  # Create database tables if they don't exist

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.query.get(int(id))

    return app


def create_database(app):
    if not os.path.exists(os.path.join(app.root_path, DB_NAME)):
        with app.app_context():
            db.create_all()
            print('Created Database!')

# Note: Replace '.views' and '.auth' with the actual package names where your views and auth blueprints are located.
