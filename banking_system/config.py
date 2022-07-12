import os

from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS =  True
    MAIL_SERVER= 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    # SECRET_KEY = os.environ.get('secretkey')
    # SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://postgres:harsh2022@localhost:5432/banking_system')
    # MAIL_SERVER= 'smtp.googlemail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('steffy.inexture@gmail.com')
    # MAIL_PASSWORD = os.environ.get('steffy!p@7069214086')
    