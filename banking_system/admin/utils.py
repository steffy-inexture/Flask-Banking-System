from functools import wraps
from flask import flash, url_for, redirect, request, current_app
from flask_login import current_user
import os
import secrets
from PIL import Image
from banking_system import db
from banking_system.models import User, Account, Transaction, TransactionType


def authentication_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
            define the decorator for authentication of particular endpoint which is used by only user
        """
        if current_user is None:
            flash("you need to login first", 'danger')
            return redirect(url_for('main.home', next=request.url))
        if current_user:
            if current_user.user_email != 'steffy.inexture@gmail.com':
                flash("only admin can has the access of that previous page", 'danger')
                return redirect(url_for('main.home', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def add_loan_money_to_user(user_id, loan_amount, loan_type):
    """
        add loan amount to the user's account balance transfer
    """
    user = User.query.filter_by(user_id=user_id).first()
    account = Account.query.filter_by(user_id=user.user_id).first()
    account.account_balance += int(loan_amount)
    transaction = Transaction(transaction_amount=loan_amount, sender_id=1, receiver_id=user.user_id, user_id=user_id)
    db.session.add(transaction)
    db.session.commit()
    transaction = Transaction.query.filter_by(transaction_amount=loan_amount, sender_id=1,
                                              receiver_id=user.user_id).first()
    loan_type_data = TransactionType(transaction_id=transaction.transaction_id, transaction_type=f'Loan-{loan_type}')
    db.session.add(loan_type_data)
    db.session.commit()


def save_picture_about(form_picture):
    """
        saves image of the bank member fetched from the form data into static pic folder
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
