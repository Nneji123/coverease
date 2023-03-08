from flask import Blueprint, redirect, render_template, request, url_for, flash, session, jsonify
from flask_login import LoginManager, current_user, login_required
from utils import generate_cover_letter
from models import Letter, db, User

from utils import generate_cover_letter, get_last_two_job_descriptions_for_user, get_num_letters_for_user, letter_history




home = Blueprint("home", __name__, template_folder="./templates", static_folder="./static")
login_manager = LoginManager()
login_manager.init_app(home)


@home.route("/home", methods=["GET"])
@login_required
def show():
    user = User.query.filter_by(email=current_user.email).first()
    number_letter = get_num_letters_for_user(user.id)
    job_descriptions = get_last_two_job_descriptions_for_user(user.id)
    letters = letter_history(user.id)
    print(number_letter, job_descriptions)
    
    return render_template("index.html", number_letter=number_letter, job_descriptions=job_descriptions,
    letters = letters)


# @home.route("/history")
# def get_history():
#     user = User.query.filter_by(email=current_user.email).first()
#     letters = letter_history(user.id)
#     return render_template("index.html", letters=letters)


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
        
        # cover_letter = generate_cover_letter(company_name=company_name, name=your_name, job_description=job_description, skills=skills)
        cover_letter="Dear CoverEase,\n\nI am writing in regards to the open position for a Software Engineer. Based on the job description, I believe that my skills and experience make me the perfect candidate for the role.\n\nAs a web developer, I am well-versed in Flask, Django, HTML, CSS, and JavaScript. I have experience building and maintaining complex web applications, and am confident that I could do the same for CoverEase. In addition, I am always keeping up-to-date with the latest web development trends and technologies, so that I can provide the best possible product to my users.\n\nI would be a valuable asset to the CoverEase team, and I am eager to put my skills to work in order to help the company achieve its goals. I look forward to discussing my qualifications further with you, and thank you for your time and consideration.\n\nSincerely,\n\nNNEJI IFEANYI DANIEL"
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
        else:
            pass
        
        return jsonify({'cover_letter': cover_letter})
        
    return render_template("index.html", num_letter=get_num_letters_for_user(current_user.id))
    