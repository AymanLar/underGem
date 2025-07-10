from flask_sqlalchemy import SQLAlchemy
from flask_user import UserMixin
from datetime import datetime
from slugify import slugify

db = SQLAlchemy()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    email_confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary='user_roles')
    genres_interested = db.Column(db.String(500), nullable=True)  # Comma-separated genres

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id', ondelete='CASCADE'))

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(100), nullable=False)
    track_title = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(50), nullable=False)
    region = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    traded = db.Column(db.Boolean, default=False)
    slug = db.Column(db.String(300))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Link to User if logged in

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        base_slug = f"{self.artist_name}-{self.track_title}"
        self.slug = slugify(base_slug) 