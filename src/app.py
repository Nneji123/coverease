import os

import css_inline
import sqlalchemy
from dotenv import load_dotenv
from flask import (Flask, abort, flash, redirect, render_template, request,
                   url_for)
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadTimeSignature
from werkzeug.security import generate_password_hash

from config import configs
from github import github_login
from googles import google_login
from home import home
from index import index, CustomIndexView
from login import login
from logout import logout
from models import User, db, UserView, Letter, LetterView
from register import register

load_dotenv()

app = Flask(__name__, template_folder="./templates", static_folder="./static")


SERVER_MODE = os.getenv("SERVER_MODE")
if SERVER_MODE in configs:
    app.config.update(configs[SERVER_MODE])
else:
    raise ValueError(f"Unknown server mode: {SERVER_MODE}")

login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)
app.app_context().push()

email = Mail(app)

app.register_blueprint(index)
app.register_blueprint(login)
app.register_blueprint(logout)
app.register_blueprint(home)
app.register_blueprint(register)
app.register_blueprint(github_login, url_prefix="/login")
app.register_blueprint(google_login, url_prefix="/signin")

serializer = URLSafeTimedSerializer("secret")

app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")


admin = Admin(
    app, name="CoverEase", template_mode="bootstrap4", index_view=CustomIndexView()
)
admin.add_view(UserView(User, db.session))
admin.add_view(LetterView(Letter, db.session))


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    try:
        return user
    except (sqlalchemy.exc.OperationalError) as e:
        return render_template("error.html", e="Database not found")


# @app.route("/500")
# def error500():
#     abort(500)


# @app.errorhandler(404)
# def not_found(e):
#     return (
#         render_template(
#             "/pages/error.html", e="The page you are looking for does not exist!"
#         ),
#         404,
#     )


# @app.errorhandler(400)
# def bad_requests(e):
#     return (
#         render_template(
#             "/pages/error.html",
#             e="The browser (or proxy) sent a request that this server could not understand.",
#         ),
#         400,
#     )


# @app.errorhandler(500)
# def internal_error(error):
#     return (
#         render_template(
#             "/pages/error.html", e="There has been an internal server error!"
#         ),
#         500,
#     )


def send_mail(to, template, subject, link, username, **kwargs):
    if os.getenv("SERVER_MODE") == "DEV":
        sender = os.getenv("DEV_SENDER_EMAIL")
    elif os.getenv("SERVER_MODE") == "PROD":
        sender = os.getenv("PROD_SENDER_EMAIL")
    msg = Message(subject=subject, sender=sender, recipients=[to])
    html = render_template(template, username=username, link=link, **kwargs)
    inlined = css_inline.inline(html)
    msg.html = inlined
    email.send(msg)


@app.route("/reset_password", methods=["POST", "GET"])
def reset_password():
    if request.method == "POST":
        mail = request.form["mail"]

        user= User.query.filter_by(email=mail).first()
        if user:
            username = user.username
        else:
            flash("User does not exist!", "danger")
            return render_template("/reset_password/index.html")

        hashCode = serializer.dumps(mail, salt="reset-password")
        user.hashCode = hashCode
        server = "http://127.0.0.1:3000" if SERVER_MODE=="DEV" else "http://coverease.live"
        link = f"{server}/{hashCode}"
        db.session.commit()
        send_mail(
            to=mail,
            template="/reset_password/email.html",
            subject="Reset Password",
            username=username,
            link=link,
        )

        flash("A password reset link has been sent to your email!", "success")
        return render_template("/reset_password/index.html")
    else:
        return render_template("/reset_password/index.html")


@app.route("/<string:hashCode>", methods=["GET", "POST"])
def hashcode(hashCode):
    try:
        mail = serializer.loads(hashCode, salt="reset-password", max_age=600)
    except BadTimeSignature:
        flash("The password reset link has expired. Please request a new one.", "danger")
        return redirect(url_for("index.show"))

    user = User.query.filter_by(email=mail).first()
    if user:
        check = user
    else:
        flash("User does not exist!", "danger")
        return render_template("/reset_password/base.html")

    if request.method == "POST":
        passw = request.form["passw"]
        cpassw = request.form["cpassw"]
        if passw == cpassw:
            check.password = generate_password_hash(passw, method="sha256")
            check.hashCode = None
            db.session.commit()
            flash("Your Password has been reset successfully!", "success")
            return redirect(url_for("login.show"))
        else:
            flash("Password fields do not match.", "danger")
            return render_template("/reset_password/reset.html", hashCode=hashCode)
    else:
        return render_template("/reset_password/reset.html", hashCode=hashCode)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=configs[SERVER_MODE]["PORT"],
        debug=configs[SERVER_MODE]["DEBUG"],
        threaded=True,
    )
