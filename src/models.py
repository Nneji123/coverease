import uuid

from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=True)
    hashCode = db.Column(db.String, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    letters = db.relationship("Letter", backref="user_letters", lazy=True, viewonly=True)


class Letter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    skills = db.Column(db.Text)
    company_name = db.Column(db.Text)
    job_description = db.Column(db.Text)

    user_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=True)
    user = db.relationship("User", backref="user_letters", lazy=True)

class LetterView(ModelView):
    column_searchable_list = ["content", "skills", "company_name", "job_description", "user_id"]
    column_filters =  ["content", "skills", "company_name", "job_description", "user_id"]


class UserView(ModelView):
    column_searchable_list = ["username", "email", "is_admin"]
    column_filters = ["username", "email", "is_admin"]
    column_exclude_list = ["password", "hashCode"]
    form_excluded_columns = ["id"]

    def on_model_change(self, form, model, is_created):
        model.password = generate_password_hash(model.password, method="sha256")
        return super(UserView, self).on_model_change(form, model, is_created)


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin