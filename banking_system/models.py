from flask import current_app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import relationship
from banking_system import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    p = User.query.get(int(user_id))
    return p


class User(db.Model, UserMixin):
    """
        User table for all user data entry with their personal information [ all data ]
    """
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(320), unique=True, nullable=False)
    user_password = db.Column(db.String(320), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    u_p = db.Column(db.String(320))
    user_phone_number = u_p
    user_first_name = db.Column(db.String(320), nullable=False)
    user_last_name = db.Column(db.String(320), nullable=False)
    user_address = db.Column(db.String(120), nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    date_of_birth = db.Column(db.DateTime, nullable=False,default=datetime.utcnow())

    user_type = relationship("UserType", cascade="all, delete", backref='user')
    account = relationship("Account", cascade="all, delete")
    transaction = relationship("Transaction", cascade="all, delete")
    loan = relationship("Loan", cascade="all, delete")
    insurance = relationship("Insurance", cascade="all, delete")

    def get_id(self):
        return self.user_id

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.user_id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):

        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.user_name}','{self.user_email}')"


class UserType(db.Model):
    """
        from User table user id associated with some user type
    """
    user_type_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    user_role = db.Column(db.String(320), nullable=False, default='user')


class Account(db.Model):
    """
        Any user from User table can have this bank account details for account
        will be stored in this Account table
    """
    account_number = db.Column(db.BigInteger, primary_key=True)
    account_status = db.Column(db.String(100), nullable=False, default='Inactive')
    account_balance = db.Column(db.Float, nullable=False, default=5000)
    saving_balance = db.Column(db.Float, nullable=False, default=0.0)
    # added
    account_creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id', ondelete='CASCADE'), nullable=False)
    account_type = relationship("AccountType", cascade="all, delete")
    fixed_deposit = relationship("FixedDeposit", cascade="all, delete")
    card = relationship("Card", cascade="all, delete")


class AccountType(db.Model):
    """
        Any bank account from Account table has account type which is stored in this
        associated with particular account id and it's type
    """
    account_type_id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.BigInteger, db.ForeignKey('account.account_number', ondelete='CASCADE'),
                               nullable=False)
    account_type = db.Column(db.String(100), nullable=False)


class Card(db.Model):
    """
        Bank user can have the card detail after getting start the bank account
    """
    card_number = db.Column(db.BigInteger, primary_key=True, default=1000)
    cvv_number = db.Column(db.Integer, nullable=False)
    card_pin = db.Column(db.Integer, nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiry_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    account_number = db.Column(db.BigInteger, db.ForeignKey('account.account_number', ondelete='CASCADE'),
                               nullable=False)


class Transaction(db.Model):
    """
        Any kind of transaction by user can store here with all details
    """
    transaction_id = db.Column(db.Integer, primary_key=True)
    transaction_amount = db.Column(db.Float, nullable=False, default=0.0)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    transaction_type = relationship("TransactionType", cascade="all, delete")


class TransactionType(db.Model):
    """
        Any transaction has transaction type like [ credit / debit / acc-to-saving .. ]
        can be stored here associated with particular transaction id and its type
    """
    transaction_type_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.transaction_id', ondelete='CASCADE'),
                               nullable=False)
    transaction_type = db.Column(db.String(100), nullable=False)


class Loan(db.Model):
    """
        User's loan details stored in Loan table
    """
    loan_id = db.Column(db.Integer, primary_key=True)
    loan_amount = db.Column(db.Integer, nullable=False, default=0.0)
    loan_status = db.Column(db.String(100), nullable=False, default='Inactive')
    rate_interest = db.Column(db.Float, nullable=False, default=0.0)
    paid_amount = db.Column(db.Float, nullable=False, default=0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    loan_type = relationship("LoanType", cascade="all, delete")


class LoanType(db.Model):
    """
        Any loan has its type which is stored in LoanType table
        can be stored here associated with particular Loan id and its type
    """
    loan_type_id = db.Column(db.Integer, primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loan.loan_id', ondelete='CASCADE'), nullable=False)
    loan_type = db.Column(db.String(100), nullable=False, default='personal loan')


class Insurance(db.Model):
    """
        User's Insurance details stored in Insurance table
    """
    insurance_id = db.Column(db.Integer, primary_key=True)
    insurance_amount = db.Column(db.Float, nullable=False, default=0.0)
    insurance_status = db.Column(db.String(100), nullable=False, default='Inactive')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    insurance_type = relationship("InsuranceType", cascade="all, delete")


class InsuranceType(db.Model):
    """
        Any Insurance has its type which is stored in InsuranceType table
        can be stored here associated with particular Insurance id and its type
    """
    insurance_type_id = db.Column(db.Integer, primary_key=True)
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurance.insurance_id', ondelete='CASCADE'), nullable=False)
    insurance_type = db.Column(db.String(100), nullable=False, default='Life')


class FixedDeposit(db.Model):
    """
        User's fd [ fixed deposit ] details stored in FixedDeposit table
    """
    fd_id = db.Column(db.Integer, primary_key=True)
    fd_amount = db.Column(db.Float, nullable=False, default=0.0)
    fd_status = db.Column(db.String(100), nullable=False, default='Inactive')
    rate_interest = db.Column(db.Float, nullable=False, default=0.0)
    fd_create_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    fd_duration = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    added_amount = db.Column(db.Float, nullable=False, default=0.0)
    account_number = db.Column(db.BigInteger, db.ForeignKey('account.account_number', ondelete='CASCADE'),
                               nullable=False)


class BankDetails(db.Model):
    """
        All bank's personal detail stored in BankDetails table
    """
    bank_name = db.Column(db.String(20), unique=True, nullable=False, default='SJK BANK')
    bank_id = db.Column(db.Integer, primary_key=True, default='1007')
    bank_email = db.Column(db.String(120), unique=True, nullable=False, default='desaiparth974@gmail.com')
    bank_contact = db.Column(db.Integer, default='10058')
    branch = relationship("Branch", cascade="all, delete")
    atm = relationship("Atm", cascade="all, delete")


class Branch(db.Model):
    """
        Bank branch detail
    """
    branch_id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(20), unique=True, nullable=False)
    branch_address = db.Column(db.String(120), unique=True, nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank_details.bank_id', ondelete='CASCADE'), nullable=False)


class Atm(db.Model):
    """
        Bank atm detail
    """
    atm_id = db.Column(db.Integer, primary_key=True)
    atm_address = db.Column(db.String(120), unique=True, nullable=False)
    bank_id = db.Column(db.Integer, db.ForeignKey('bank_details.bank_id', ondelete='CASCADE'), nullable=False)


class BankMember(db.Model):
    """
        All bank member detail
    """
    image_file = db.Column(db.Text, nullable=False)
    bank_member_id = db.Column(db.Integer, primary_key=True)
    bank_member_name = db.Column(db.String, nullable=False)
    bank_member_position = db.Column(db.String, nullable=False, default='Bank member')
    bank_member_about = db.Column(db.String(320))
    bank_member_email_id = db.Column(db.String(320), nullable=False)
    bank_member_contact = db.Column(db.BigInteger, nullable=False)


class MemberRole(db.Model):
    """
        Member role details list
    """
    id = db.Column(db.Integer, primary_key=True)
    member_role = db.Column(db.String)


class LoanDetails(db.Model):
    """
        Loan choices detail
    """
    id = db.Column(db.Integer, primary_key=True)
    loan_name = db.Column(db.String)


class InsuranceDetails(db.Model):
    """
        Insurance choices list
    """
    id = db.Column(db.Integer, primary_key=True)
    insurance_name = db.Column(db.String)


class OtpByMail(db.Model):
    """
        Temporary stores the otp which is sent to mail address [ for transaction purpose ]
        deleted after usage
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), nullable=False)
    otp = db.Column(db.Integer, nullable=False)
