from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from banking_system.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['CELERYBEAT_SCHEDULE'] = {
        # Executes every minute
        'celery_example.fd_data': {
            'task': 'celery_example.fd_data',
        }
    }
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from banking_system.users.routes import users
    from banking_system.main.routes import main
    from banking_system.about.routes import about
    from banking_system.admin.routes import admin
    from banking_system.errors.handlers import errors
    from demo1 import demo

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(about)
    app.register_blueprint(admin)
    app.register_blueprint(errors)
    app.register_blueprint(demo)


    return app
