from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

login_manager = LoginManager()

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    app.config['SECRET_KEY'] = 'this_is_a_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'

    db.init_app(app)
    # login_manager.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    with app.app_context():
        from .main import main as main_blueprint
        from .auth import auth as auth_blueprint
        print("creating db")

        # blueprint for auth.py routes in our app
        app.register_blueprint(auth_blueprint)

        # blueprint for non-auth.py parts of app
        app.register_blueprint(main_blueprint)

        db.create_all()

        return app
