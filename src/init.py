import os
from typing import Union

from dotenv import load_dotenv
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from app import db
from models import User

load_dotenv()


def create_user(username: str, email: str, password: str, is_admin):
    password = generate_password_hash(password, method="sha256")
    try:
        new_user = User(username=username, email=email, password=password, is_admin=is_admin)
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    return new_user


def main():
    # make_dirs()
    db.create_all()
    create_user("Ifeanyi", "ifeanyinneji777@gmail.com", "linda321", is_admin=False)
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
    create_user(username=ADMIN_USERNAME,email = ADMIN_EMAIL, password=ADMIN_PASSWORD, is_admin = True)


if __name__ == "__main__":
    main()
