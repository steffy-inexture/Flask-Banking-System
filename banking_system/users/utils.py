import random
from flask import flash
from flask_login import current_user
from flask_mail import Message
from validate_email_address import validate_email
from wtforms import ValidationError
from banking_system import mail, db
from banking_system.models import User, UserType, LoanType, Insurance, InsuranceType, TransactionType, \
    OtpByMail

from functools import wraps
from flask import request, redirect, url_for


def send_reset_email(user):
    """
        SEND MAIL TO CURRENT USER'S MAIL ID
        for changing the user's password
    """
    token = user.get_reset_token()
    msg = Message('Password REset Request', sender='steffykhristi.18.ce@iite.indusuni.ac.in',
                  recipients=[user.user_email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then just ignore this msg and no change will be there.   
'''
    mail.send(msg)


def send_otp_email(user):
    """
        SEND MAIL TO CURRENT USER'S MAIL ID
        for transaction otp
    """

    otp = random.randint(1111, 9999)
    msg = Message('Your OTP is here: ', sender='steffykhristi.18.ce@iite.indusuni.ac.in',
                  recipients=[user.user_email])
    msg.body = f'''This is the OTP as requested: :{otp}
    Kindly check the next page and enter the otp.
    If you did not make this request then just ignore this msg and no change will be there.
    '''
    mail.send(msg)
    data = OtpByMail(email=user.user_email, otp=otp)
    db.session.add(data)
    db.session.commit()

    return otp


class CustomValidation:
    """
        custom validations for form fields validation check which is repeated
    """

    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user:
            raise ValidationError('That username is taken please Choose different one')

    def validate_user_email(self, user_email):
        isvalid = validate_email('user_email.data', verify=True)
        email = User.query.filter_by(user_email=user_email.data).first()
        if email:
            raise ValidationError('That email is taken please Choose different one')
        if isvalid:
            raise ValidationError('This email id is not exist')


# user route's functions starts

def role_assign(user_id):
    """
        assign the role of any user [ bank user / bank admin ]
    """
    user_role = UserType(user_id=user_id, user_role='user')
    db.session.add(user_role)
    db.session.commit()


def add_loan_type(loan_type, loan_id):
    """
        After applying for loan add the type of loan to loantype table with loan id data
    """
    loan_type = str(loan_type)
    loan = LoanType(loan_id=loan_id, loan_type=loan_type)
    db.session.add(loan)
    db.session.commit()

def insurance_type(insurance_type_):
    """
        Add type of insurance after applying for the insurance
    """
    insurance = Insurance.query.filter_by(user_id=current_user.user_id).first()
    insurance_type = InsuranceType(insurance_id=insurance.insurance_id, insurance_type=insurance_type_)
    db.session.add(insurance_type)
    db.session.commit()


def add_transaction_type(transaction_type, transaction_id):
    """
        add type of transaction after Transaction of money
    """
    find_type = TransactionType.query.filter_by(transaction_id=transaction_id).first()
    if find_type:
        pass
    else:
        add_type = TransactionType(transaction_id=transaction_id,
                                   transaction_type=transaction_type)
        db.session.add(add_type)
        db.session.commit()


# user route's functions ends


# define the decorator for authentication of particular endpoint
def authentication_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user is None:
            flash("you need to login first", 'danger')
            return redirect(url_for('main.home', next=request.url))
        if current_user:
            if current_user.user_email != 'steffy.inexture@gmail.com':
                flash("only admin can has the access of that previous page", 'danger')
                return redirect(url_for('main.home', next=request.url))
        return f(*args, **kwargs)

    return decorated_function

# define the decorator for authentication of particular endpoint weather the login has been done by the particulare user only
def user_auth(f):
    @wraps(f)
    def decorator_fun(*args, **kwargs):
        if current_user is None:
            flash("you need to login first", 'danger')
            return redirect(url_for('main.home', next=request.url))
        if current_user:
            user_type=UserType.query.filter_by(user_id=current_user.user_id).first()
            if not user_type.user_role == 'user':
                flash("only user can has the access that page", 'danger')
                return redirect(url_for('main.home', next=request.url))
        return f(*args, **kwargs)

    return decorator_fun



