import uuid

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=True)
    picture = db.Column(db.String)
    letters = db.relationship('Letter', backref='user_letters', lazy=True)

class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    skills = db.Column(db.Text)
    company_name = db.Column(db.Text)
    job_description = db.Column(db.Text)
    
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)
    user = db.relationship('User', backref='user_letters', lazy=True)