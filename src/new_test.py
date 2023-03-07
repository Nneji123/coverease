# import os
# from flask import Flask, redirect, url_for
# from flask_dance.contrib.google import make_google_blueprint, google
# from dotenv import load_dotenv

# load_dotenv()

# app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersekrit")
# app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
# app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
# google_bp = make_google_blueprint(scope=["profile", "email"])
# app.register_blueprint(google_bp, url_prefix="/login")

# @app.route("/")
# def index():
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     resp = google.get("/oauth2/v1/userinfo")
#     assert resp.ok, resp.text
#     print(resp.json()["email"], resp.json()["picture"], resp.json()["given_name"])
#     return "You are {email} on Google".format(email=resp.json()["email"])

import os
from flask import Flask, redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")


@app.route("/")
def index():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    print(resp.json())
    return "You are @{login} on GitHub".format(login=resp.json()["login"])



if __name__=="__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")