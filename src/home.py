from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, current_user, login_required




home = Blueprint("home", __name__, template_folder="./templates", static_folder="./static")
login_manager = LoginManager()
login_manager.init_app(home)


@home.route("/home", methods=["GET"])
@login_required
def show():
    return render_template("index.html")