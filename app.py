from flask import Flask
from flask_user import UserManager
import os
from models import db, User
from constants import SECRET_KEY, DATABASE_URI, USER_EMAIL_SENDER_EMAIL
from routes import init_routes
from commands import init_commands

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['USER_EMAIL_SENDER_EMAIL'] = os.environ.get('USER_EMAIL_SENDER_EMAIL', USER_EMAIL_SENDER_EMAIL)

    # Initialize extensions
    db.init_app(app)
    
    # Setup Flask-User
    user_manager = UserManager(app, db, User)
    
    # Initialize routes and commands
    init_routes(app)
    init_commands(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
