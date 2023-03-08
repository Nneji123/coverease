import os

from dotenv import load_dotenv

load_dotenv()


POSTGRES = os.getenv("POSTGRES")
SQLITE = os.getenv("SQLITE")

configs = {
    "PROD": {
        "SQLALCHEMY_DATABASE_URI": POSTGRES,
        "LOGIN_DISABLED": False,
        "PORT": 3000,
        "DEBUG": False,
        # "SERVER_NAME": "http://coverease.live",
        "MAIL_SERVER": os.getenv("PROD_MAIL_SERVER"),
        "MAIL_PORT": os.getenv("PROD_MAIL_PORT"),
        "MAIL_USERNAME": os.getenv("PROD_MAIL_USERNAME"),
        "MAIL_PASSWORD": os.getenv("PROD_MAIL_PASSWORD"),
        "MAIL_USE_TLS": True,
        "MAIL_USE_SSL": False,
        "SECRET_KEY": os.getenv("PROD_SECRET_KEY"),
    },
    "DEV": {
        "SQLALCHEMY_DATABASE_URI": SQLITE,
        "LOGIN_DISABLED": True,
        "PORT": 3000,
        "DEBUG": True,
        # "SERVER_NAME": "http://127.0.0.1:3000",
        "MAIL_SERVER": os.getenv("DEV_MAIL_SERVER"),
        "MAIL_PORT": int(os.getenv("DEV_MAIL_PORT")),
        "MAIL_USERNAME": os.getenv("DEV_MAIL_USERNAME"),
        "MAIL_PASSWORD": os.getenv("DEV_MAIL_PASSWORD"),
        "MAIL_USE_TLS": True,
        "MAIL_USE_SSL": False,
        "SECRET_KEY": os.getenv("DEV_SECRET_KEY"),
    },
}
