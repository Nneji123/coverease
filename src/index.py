from flask import Blueprint, redirect, url_for, render_template
from flask_admin import expose
from flask_login import logout_user

# from models import MyAdminIndexView

index = Blueprint("index", __name__, template_folder="./templates")


@index.route("/", methods=["GET"])
def show():
    return render_template("home.html")


# class CustomIndexView(MyAdminIndexView):
#     @expose("/logout")
#     def logout(self):
#         logout_user()
#         return redirect(url_for("login.show"))
