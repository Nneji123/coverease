import os

import sqlalchemy
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
import sqlalchemy


from models import db, User

from dotenv import load_dotenv

load_dotenv()


register = Blueprint("register", __name__, template_folder="./frontend")
login_manager = LoginManager()
login_manager.init_app(register)

    

@register.route("/register", methods=["GET", "POST"])
def show():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]

        if username and email and password and confirm_password:
            if password == confirm_password:
                hashed_password = generate_password_hash(password, method="sha256")
                user = bool(User.query.filter_by(email=email).first())
                if user == False:
                    try:
                        new_user = User(
                            username=username,
                            email=email,
                            password=hashed_password,
                        )
                        db.session.add(new_user)
                        db.session.commit()
                        flash("You have successfully registered!", "success")
                        return redirect(url_for("login.show") + "?success=account-created")
                    except sqlalchemy.exc.IntegrityError:
                        db.session.rollback()
                        flash("User already exists!", "failure")
                        return redirect(
                            url_for("register.show") + "?error=user-or-email-exists"
                        )
                    finally:
                        db.session.close()
                elif user:
                    flash("User already exists!", "failure")
                    return redirect(url_for("register.show") + "?error=user-or-email-exists")
        else:
            flash("Please fill in all fields!", "failure")
            return redirect(url_for("register.show") + "?error=missing-fields")
    else:
        return render_template("register.html")