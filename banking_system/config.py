import os
from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    # for usage of redis [ delete if you are not using this ]
    # CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
    # app.config['CELERY_BACKEND'] = 'redis://127.0.0.1:6379'
    # CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'


