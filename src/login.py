from flask import redirect, url_for, render_template, request, flash, Blueprint, session
from flask_login import login_user, LoginManager
from werkzeug.security import check_password_hash
from models import User
from dotenv import load_dotenv

from utils import get_num_letters_for_user

load_dotenv()

login = Blueprint(
    "login", __name__, template_folder="./templates", static_folder="./static"
)
login_manager = LoginManager()
login_manager.init_app(login)



@login.route("/logins", methods=["GET", "POST"])
def show():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                flash("You are logged in.")
                print("You are logged in!")
                picture="./static/images/profile_icon.png"
                session["picture"] = picture
                session["email"] = email
                session["username"] = user.username
                return redirect(url_for("home.show"))
            else:
                flash("Incorrect password. Please try again.")
                return redirect(url_for("login.show") + "?error=incorrect-password")
        else:
            flash("You are not registered with us. Please register first.")
            return redirect(url_for("login.show") + "?error=user-not-found")
    else:
        return render_template("login.html")