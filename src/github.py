import os
from flask import Flask, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_dance.contrib.github import make_github_blueprint, github
from dotenv import load_dotenv
from models import GithubUser, db
import sqlalchemy

load_dotenv()

github_login = make_github_blueprint(redirect_to="github.index")
# app.register_blueprint(github_bp, url_prefix="/login")

@github_login.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    email = resp.json()['email']
    username = resp.json()['name']
    picture = resp.json()['avatar_url']
    print(resp)
    print(picture, email, username)
    user = GithubUser.query.filter_by(email=email).first()
    if user:
        login_user(user)
        return redirect(url_for('home.show'))
    else:
        try:
            new_user = GithubUser(username=username, email=email, picture=picture)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home.show'))
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()
    # flash("Unauthorized!", "danger")
    # return redirect(url_for("login.show"))
