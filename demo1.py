from random import choice
from flask import Flask, flash, url_for, Blueprint
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from banking_system import db
from banking_system.models import Account, FixedDeposit, Transaction, TransactionType, User
from banking_system.users.constants import LOGIN_FIRST, FLASH_MESSAGES, PENDING_ACTIVITY, SUCCESS_ACTIVITY
from banking_system.users.utils import user_auth
from flask_celery import make_celery
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

demo = Blueprint('demo', __name__)

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379'
# app.config['CELERY_BACKEND'] = 'redis://127.0.0.1:6379'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379'
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:harsh2022@localhost:5432/celery_example"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

celery = make_celery(app)

@demo.route("/user/add_fixed_deposit", methods=['GET', 'POST'])
@login_required
@user_auth
def add_fixed_deposit():
    """
        Add fixed deposit by using ths route
        goes to the admin side with INACTIVE Status [ initially ]
        redirects to: users.dashboard [ user route ] (if succeed)
                      users.main [ user route ] (if not succeed)
    """

    if current_user.is_authenticated:
        account = Account.query.filter_by(user_id=current_user.user_id).first()
        is_already_fd_exist = FixedDeposit.query.filter_by(account_number=account.account_number).first()
        if not is_already_fd_exist:
            fixed_deposit = FixedDeposit(account_number=account.account_number)
            db.session.add(fixed_deposit)
            db.session.commit()
            u_d=current_user.user_id
            fd_money_by_celery.delay(u_d)
            flash(SUCCESS_ACTIVITY.format(activity='FIXED DEPOSIT'), FLASH_MESSAGES['SUCCESS'])
            return redirect(url_for('users.dashboard'))
        else:
            flash(PENDING_ACTIVITY.format(activity='FIXED DEPOSIT'), FLASH_MESSAGES['FAIL'])
            return redirect(url_for('users.dashboard'))
    else:
        flash(LOGIN_FIRST, FLASH_MESSAGES['FAIL'])
        return redirect('main.home')

@celery.task(name='celery_example.fd_data')
def fd_money_by_celery(user_id):
    """
            add the interested money which is get by particular time duration
            only after admin activated the fd
        """
    print('TEST **********************')
    user=User.query.filter_by(user_id=user_id)
    account = Account.query.filter_by(user_id=user.user_id).first()
    fd = FixedDeposit.query.filter_by(account_number=account.account_number).first()
    account.account_balance += ((fd.fd_amount * fd.rate_interest) / 100)
    transaction = Transaction(transaction_amount=((fd.fd_amount * fd.rate_interest) / 100),
                              sender_id=user.user_id,receiver_id=user.user_id,
                              user_id=user.user_id)
    db.session.add(transaction)
    db.session.commit()
    transaction_type = TransactionType(transaction_id=transaction.transaction_id,
                                       transaction_type="fd refund RI")
    db.session.add(transaction_type)
    db.session.commit()
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

#
#
# class Results(db.Model):
#     id = db.Column('id', db.Integer, primary_key=True)
#     data = db.Column('data', db.String(50))

#
# @app.route('/process/<name>')
# def process(name):
#     reverse.delay(name)
#     return 'I sent an async request!'
#
# @app.route('/insertData')
# def insertData():
#     inserti.delay()
#
#     return 'I sent an async request to insert data into database.'
#
# @celery.task(name='celery_example.reverse')
# def reverse(string):
#     return string[::-1]
#
# @celery.task(name='celery_example.inserti')
# def inserti():
#
#     for i in range(500):
#         data = ''.join(choice('ABC') for i in range(10))
#         result = Results(data=data)
#
#         db.session.add(result)
#
#     db.session.commit()


# if __name__ == '__main__':
#     app.run(debug=True)
