import uuid

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    letters = db.relationship('Letter', backref='user_letters', lazy=True)
    
class GoogleUser(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    picture = db.Column(db.String)
    
    google_letters = db.relationship('Letter', backref='googleuser_letters', lazy=True)

class GithubUser(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    picture = db.Column(db.String)
    
    github_letters = db.relationship('Letter', backref='githubuser_letters', lazy=True, overlaps="githubuser_letters")

class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    skills = db.Column(db.Text)
    company_name = db.Column(db.Text)
    job_description = db.Column(db.Text)
    
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='user_letters', lazy=True)
    
    google_user_id = db.Column(db.String(36), db.ForeignKey('google_user.id'), nullable=True)
    google_user = db.relationship('GoogleUser', backref='googleuser_letters', lazy=True)
    
    github_user_id = db.Column(db.String(36), db.ForeignKey('github_user.id'), nullable=True)
    github_user = db.relationship('GithubUser', backref='githubuser_letters', lazy=True, overlaps="githubuser_letters")
