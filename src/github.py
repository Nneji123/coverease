import os

import sqlalchemy
from dotenv import load_dotenv
from flask import flash, redirect, session, url_for
from flask_dance.contrib.github import github, make_github_blueprint
from flask_login import login_user

from models import User, db

load_dotenv()

github_login = make_github_blueprint(redirect_to="github.index")


@github_login.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    email = resp.json()["email"]
    username = resp.json()["name"]
    picture = resp.json()["avatar_url"]

    session["picture"] = picture
    session["email"] = email
    session["username"] = username
    user = User.query.filter_by(email=email).first()
    if user:
        login_user(user)
        return redirect(url_for("home.show"))
    else:
        try:
            new_user = User(username=username, email=email, picture=picture)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("home.show"))
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()
    flash("Unauthorized!", "danger")
    return redirect(url_for("login.show"))