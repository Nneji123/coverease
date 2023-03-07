
import os
from typing import Union

from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import db
from models import User

load_dotenv()


def create_user(username, email, password):
    password = generate_password_hash(password, method="sha256")
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def main():
    # make_dirs()
    db.create_all()
    create_user("Ifeanyi", "ifeanyinneji777@gmail.com", "linda321")
    # create_new_user(
    #     type_of_user="lecturer",
    #     username="OGUNLADE",
    #     email="ogunlade@gmail.com",
    #     password="password",
    #     role="lecturer",
    # )
    # create_new_user(
    #     type_of_user="student",
    #     username="NNEJI IFEANYI DANIEL",
    #     email="ifeanyinneji777@gmail.com",
    #     password="password",
    #     matric_number="19 ENG02 077",
    #     role="student",
    # )
    # ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    # ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    # ADMIN_ROLE = os.getenv("ADMIN_ROLE")
    # create_new_user(
    #     type_of_user="admin",
    #     username=ADMIN_USERNAME,
    #     password=ADMIN_PASSWORD,
    #     role=ADMIN_ROLE,
    # )


if __name__ == "__main__":
    main()
