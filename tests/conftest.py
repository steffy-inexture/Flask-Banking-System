import pytest
from flask import template_rendered

from banking_system import db, create_app
from banking_system.models import BankDetails, Branch, LoanDetails, InsuranceDetails, MemberRole, User, UserType, \
    Account, AccountType, Card, Transaction, TransactionType, Loan, LoanType, Insurance, InsuranceType, FixedDeposit, \
    Atm, BankMember, OtpByMail
from datetime import datetime


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "DEBUG": True,
        "WTF_CSRF_ENABLED": False,
    })
    ctx = app.test_request_context()

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with app.app_context():
        db.create_all()

        bank_data = BankDetails(
            bank_id=1,
            bank_name='BankTest',
            bank_email='steffy.inexture@gmail.com',
            bank_contact=12345,
        )

        db.session.add(bank_data)
        db.session.commit()

        branch_data = Branch(
            branch_id=1,
            branch_name='test branch',
            branch_address='test b-address',
            bank_id=1
        )

        not_associate_bank_branch = Branch(
            branch_id=2,
            branch_name='not branch associated',
            branch_address='dummy data',
            bank_id=1
        )
        db.session.add(not_associate_bank_branch)
        db.session.add(branch_data)

        atm = Atm(atm_id=1, atm_address='ahmedabad', bank_id=1)
        db.session.add(atm)
        db.session.commit()

        loan_choice = LoanDetails(loan_name='test loan choice1')
        insurance_choice = InsuranceDetails(insurance_name='test insurance choice1')
        bank_member_choice = MemberRole(member_role='test role1')
        db.session.add(loan_choice)
        db.session.add(insurance_choice)
        db.session.add(bank_member_choice)

        user1 = User(
            user_id=1, user_name='steffy', user_password='steffy@123',
            user_email='steffy.jk2018@gmail.com', u_p=1234567898, user_first_name='steffy',
            user_last_name='jk', user_address='407,NYC', user_age=21,
            date_of_birth=datetime.utcnow()
        )

        user2 = User(
            user_id=2, user_name='stella', user_password='stella@123',
            user_email='stella.jk2018@gmail.com', u_p=1234567898, user_first_name='stella',
            user_last_name='jk', user_address='407,NYC', user_age=21,
            date_of_birth=datetime.utcnow()
        )

        inactive_user = User(
            user_id=5, user_name='inactive', user_password='inactive@123',
            user_email='inactive.jk2018@gmail.com', u_p=1234567898, user_first_name='inactive',
            user_last_name='jk', user_address='407,NYC', user_age=21,
            date_of_birth=datetime.utcnow()
        )

        admin = User(
            user_id=3, user_name='admin', user_password='admin@123',
            user_email='steffy.inexture@gmail.com', u_p=1234567898, user_first_name='admin',
            user_last_name='jk', user_address='407,NYC', user_age=21,
            date_of_birth=datetime.utcnow()
        )

        db.session.add(user1)
        db.session.add(user2)
        db.session.add(admin)
        db.session.add(inactive_user)
        db.session.commit()

        user_type1 = UserType(user_id=user1.user_id,
                              user_role='user')
        admin_type = UserType(user_id=admin.user_id,
                              user_role='admin')

        inactive_type = UserType(user_id=inactive_user.user_id,
                                 user_role='user')
        db.session.add(user_type1)
        db.session.add(admin_type)
        db.session.add(inactive_type)
        db.session.commit()

        account_user1 = Account(
            account_number=1000000,
            account_status='Active',
            account_balance=5000,
            saving_balance=0,
            account_creation_date=datetime.utcnow(),
            user_id=1,
            branch_id=1
        )
        db.session.add(account_user1)

        account_user2 = Account(
            account_number=1000001,
            account_status='Active',
            account_balance=5000,
            saving_balance=0,
            account_creation_date=datetime.utcnow(),
            user_id=2,
            branch_id=1
        )
        inactive_acc = Account(
            account_number=1000005,
            account_status='Inactive',
            account_balance=5000,
            saving_balance=0,
            account_creation_date=datetime.utcnow(),
            user_id=5,
            branch_id=1
        )
        db.session.add(account_user2)
        db.session.add(inactive_acc)
        db.session.commit()

        card1 = Card(card_number=1, cvv_number=1234, card_pin=1234, creation_date=datetime.utcnow(),
                     expiry_date=datetime.utcnow(), account_number=1000000)

        db.session.add(card1)

        loan1 = Loan(loan_id=1, loan_amount=5000, loan_status='Active', rate_interest=5.6,
                     paid_amount=0, user_id=1)
        loan_type1 = LoanType(loan_type_id=1, loan_id=1, loan_type='personal loan')
        insurance1 = Insurance(insurance_id=1, insurance_amount=5000, insurance_status='Active', user_id=1)
        insurance_type1 = InsuranceType(insurance_type_id=1, insurance_id=1, insurance_type='life insurance')
        fd1 = FixedDeposit(fd_id=1, fd_amount=5000, fd_status='Active', rate_interest=5.6,
                           fd_create_date=datetime.utcnow(), fd_duration=datetime.utcnow(),
                           added_amount=0, account_number=1000000)
        db.session.add(insurance_type1)
        db.session.add(loan1)
        db.session.add(loan_type1)
        db.session.add(insurance1)
        db.session.add(fd1)
        db.session.commit()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

# ---------------test model.py's model start----------------------------------
@pytest.fixture()
def new_user():
    user = User(
        user_name='testuser',
        user_password='testuser@123',
        user_email='testuser@gmail.com',
        u_p=1234567888,
        user_first_name='test',
        user_last_name='user',
        user_address='NYC',
        user_age=21,
        date_of_birth=datetime.utcnow()
    )
    return user


@pytest.fixture()
def new_user_type():
    user_type = UserType(user_id=1, user_role='user')
    return user_type


@pytest.fixture()
def new_account():
    account = Account(
        account_number=1,
        user_id=1,
        branch_id='1'
    )
    return account


@pytest.fixture()
def new_account_type():
    account_type = AccountType(
        account_type_id=1,
        account_number=1,
        account_type='Active'
    )
    return account_type


@pytest.fixture()
def new_card():
    card = Card(
        card_number=1000,
        cvv_number=1000,
        card_pin=1234,
        creation_date=datetime.utcnow(),
        expiry_date=datetime.utcnow(),
        account_number=1
    )
    return card


@pytest.fixture()
def new_transaction():
    transaction = Transaction(
        transaction_id=1,
        transaction_amount=1000,
        sender_id=1,
        receiver_id=1,
        transaction_date=datetime.utcnow(),
        user_id=1,
    )
    return transaction


@pytest.fixture()
def new_transaction_type():
    transaction_type = TransactionType(
        transaction_type_id=1,
        transaction_id=1,
        transaction_type='Credit'
    )
    return transaction_type


@pytest.fixture()
def new_loan():
    loan = Loan(
        loan_id=1,
        loan_amount=100,
        loan_status='Active',
        rate_interest=5.6,
        paid_amount=5,
        user_id=1,
    )
    return loan


@pytest.fixture()
def new_loan_type():
    loan_type = LoanType(
        loan_type_id=1,
        loan_id=1,
        loan_type='Car loan'
    )

    return loan_type


@pytest.fixture()
def branch_data(app):
    data = Branch(
        branch_name='Iskon',
        branch_address='3,ahemdabad',
        bank_id=1,
    )
    return data


@pytest.fixture()
def new_insurance():
    insurance = Insurance(
        insurance_id=1,
        insurance_amount=10000,
        insurance_status='Active',
        user_id=1
    )
    return insurance


@pytest.fixture()
def new_insurance_type():
    insurance_type = InsuranceType(
        insurance_type_id=1,
        insurance_id=1,
        insurance_type='Life insurance'
    )
    return insurance_type


@pytest.fixture()
def new_fixed_deposit():
    fd = FixedDeposit(
        fd_id=1,
        fd_amount=10000,
        fd_status='Active',
        rate_interest=5.6,
        fd_create_date=datetime.utcnow(),
        fd_duration=datetime.utcnow(),
        added_amount=5000,
        account_number=1,
    )
    return fd


@pytest.fixture()
def new_bank_details():
    bank = BankDetails(
        bank_name='demobank',
        bank_id=5,
        bank_email='demo122@gmail.com',
        bank_contact=12345
    )
    return bank


@pytest.fixture()
def new_branch():
    branch = Branch(
        branch_id=1,
        branch_name='sjk',
        branch_address='ahmedabad',
        bank_id=1
    )
    return branch


@pytest.fixture()
def new_atm():
    atm = Atm(
        atm_id=1,
        atm_address='ahmedabad',
        bank_id=1
    )
    return atm


@pytest.fixture()
def new_bank_member():
    member = BankMember(
        image_file="testprofile.jpg",
        bank_member_id=1,
        bank_member_name='steffy',
        bank_member_position='user',
        bank_member_about='hey this is steffy,nice to meet ya',
        bank_member_email_id='user@gmail.com',
        bank_member_contact=1234567895
    )
    return member


@pytest.fixture()
def new_member_role():
    role = MemberRole(
        id=1,
        member_role='bank user'
    )
    return role


@pytest.fixture()
def new_loan_detail():
    loan_detail = LoanDetails(id=1, loan_name='home loan')
    return loan_detail


@pytest.fixture()
def new_insurance_detail():
    insurance_detail = InsuranceDetails(id=1, insurance_name='home loan')
    return insurance_detail


@pytest.fixture()
def otp_by_mail():
    otp = OtpByMail(id=1, email='home@gmail.com', otp=1234)
    return otp


# ---------------testing for models.py end here-------------------------------------------------
# ------------------------------------------------------

@pytest.fixture()
def login(client):
    """Login helper function"""
    response = client.post(
        "/login",
        data=dict(
            user_id=1,
            user_name='steffy',
            user_email='steffy.jk2018@gmail.com',
            user_password='steffy@123',
            remember='y'),
        follow_redirects=True
    )
    return response


@pytest.fixture()
def admin_login(client):
    """admin Login helper function"""
    response = client.post(
        "/admin_login/",
        data=dict(
            user_id=3,
            user_name='admin',
            user_email='steffy.inexture@gmail.com',
            user_password='admin@123',
            remember='y'),
        follow_redirects=True
    )
    return response


@pytest.fixture()
def login2(client):
    """Login helper function"""
    response = client.post(
        "/login",
        data=dict(
            user_id=2,
            user_email='stella.jk2018@gmail.com',
            user_password='stella@123',
            remember='y'),
        follow_redirects=True
    )
    return response


@pytest.fixture()
def login_fake(client):
    """Login helper function"""
    response = client.post(
        "/login",
        data=dict(
            user_id=1,
            user_email='stellak.jk2018@gmail.com',
            user_password='steffy@123',
            remember='y'),
        follow_redirects=True
    )
    return response


@pytest.fixture()
def inactive_login(client):
    """Login helper function"""
    response = client.post(
        "/login",
        data=dict(
            user_id=1,
            user_email='inactive.jk2018@gmail.com',
            user_password='inactive@123',
            remember='y'),
        follow_redirects=True
    )
    return response


# ----------------------------------------------
