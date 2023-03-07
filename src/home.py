from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, current_user, login_required
from utils import generate_cover_letter
from models import Letter, db, User, GithubUser, GoogleUser




home = Blueprint("home", __name__, template_folder="./templates", static_folder="./static")
login_manager = LoginManager()
login_manager.init_app(home)


@home.route("/home", methods=["GET"])
@login_required
def show():
    return render_template("index.html")

@home.route("/generate", methods=["GET","POST"])
@login_required
def generate():
    if request.method == "POST":
        job_description = request.form["job_description"]
        your_name = request.form["name"]
        company_name = request.form["company_name"]
        skills = request.form["skills"]
        
        # get the currently authenticated user
        user = User.query.filter_by(email=current_user.email).first()
        googleuser = GoogleUser.query.filter_by(email=current_user.email).first()
        githubuser = GithubUser.query.filter_by(email=current_user.email).first()
        cover_letter = generate_cover_letter(company_name=company_name, name=your_name, job_description=job_description, skills=skills)
        
        if user:
            letter = Letter(
            content=cover_letter,
            skills=skills,
            company_name=company_name,
            job_description=job_description,
            user=user,
            )
            db.session.add(letter)
            db.session.commit()
        elif googleuser:
            letter = Letter(
            content=cover_letter,
            skills=skills,
            company_name=company_name,
            job_description=job_description,
            google_user=googleuser,
            )
            db.session.add(letter)
            db.session.commit()
        elif githubuser:
            letter = Letter(
            content=cover_letter,
            skills=skills,
            company_name=company_name,
            job_description=job_description,
            github_user=githubuser,
            )
            db.session.add(letter)
            db.session.commit()
    return render_template("index.html", cover_letter=cover_letter)

    