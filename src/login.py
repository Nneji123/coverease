import os
from flask import Flask, redirect, url_for, render_template, request, flash, Blueprint
from flask_login import login_user, logout_user, login_required, LoginManager
from werkzeug.security import check_password_hash
from models import db, User
from dotenv import load_dotenv

load_dotenv()

login = Blueprint(
    "login", __name__, template_folder="./templates", static_folder="./static"
)
login_manager = LoginManager()
login_manager.init_app(login)



@login.route("/login", methods=["GET", "POST"])
def show():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                if user.is_admin:
                    login_user(user, remember=True)
                    return redirect(url_for("admin.show"))
                else:
                    login_user(user)
                    next_page = request.args.get('next')
                    flash("You are logged in.")
                    print("You are logged in!")
                    return redirect(next_page) if next_page else redirect(url_for('home.show'))
            else:
                flash("Incorrect password. Please try again.")
                return redirect(url_for("login.show") + "?error=incorrect-password")
        else:
            flash("You are not registered with us. Please register first.")
            return redirect(url_for("login.show") + "?error=user-not-found")
    else:
        return render_template("login.html")