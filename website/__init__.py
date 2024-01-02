# makes the website folder a Python package
# means you can import the folder, init.py would run automatically
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "testing"

    # choose location where to create db
    db_path = os.path.join(os.path.dirname(__file__), DB_NAME)
    db_uri = 'sqlite:///{}'.format(db_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

    # initializes db
    db.init_app(app)

    # register routes from these files
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # creates db without overwriting existing file
    from .models import User, Post, Comment
    with app.app_context():
        db.create_all()

    # set up login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' # default page
    login_manager.init_app(app)

    # loading users
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app