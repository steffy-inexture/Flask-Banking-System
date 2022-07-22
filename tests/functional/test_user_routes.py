from datetime import datetime

from flask import session
from flask_login import current_user
from wtforms import form


def test_registration(client):
    response = client.post("/user/registration",
                           data=dict(
                               user_id=7, user_name='sdfghjk', user_email='vacationsfever2021@gmail.com',
                               user_phone_number=1234567895, user_first_name='steff',
                               user_last_name='steffjk', user_address='407,NYC',
                               user_age=21, date_of_birth=datetime.utcnow(),
                               user_password='steff@123', confirm_password='steff@123',
                               role_assign=True, account_creation=True
                           ), follow_redirects=True
                           )
    assert response.status_code == 200
    # assert 'Your account has been created you are all set for login' in str(response.data)


# def test_registration_with_admin(client,admin_login):
#     response = client.post("/user/registration",
#                            data=dict(
#                                user_id=7, user_name='steff', user_email='steff@gmail.com',
#                                user_phone_number=1234567894, user_first_name='steff',
#                                user_last_name='steffjk', user_address='407,NYC',
#                                user_age=21, date_of_birth=datetime.utcnow(),
#                                user_password='steff@123', confirm_password='steff@123',
#                                role_assign=True, account_creation=True
#                            ), follow_redirects=True
#                            )
#
#     assert 'steffy.inexture@gmail.com' in str(admin_login.data)
#     print("8888888888888888888888",admin_login.data)
#     if current_user.user_email == 'steffy.inexture@gmail.com':
#         assert 'New user added successfully' in str(response.data)


def test_login(login):
    assert 'Login successfully' in str(login.data)
    assert login.status_code == 200
    assert login.request.path == "/user-dashboard"


# test wrong login data
def test_wrong_credentials(login_fake):
    assert 'Login unsuccessfully..please check email and password' in str(login_fake.data)
    assert login_fake.status_code == 200


def test_dashboard(client, login):
    data = client.get(
        "/user-dashboard",
        data=dict(
            transaction=None,
            transaction_type='Credit',
            loan=1,
            insurance=2,
            fixed_deposit=3),
        follow_redirects=True

    )
    assert data.status_code == 200


def test_profile_get(client):
    response = client.get(
        "/login",
        data=dict(
            user_name='steff',
            user_phone_number=1234567895,
            user_first_name='steff',
            user_last_name='jk',
            user_age=21,
            user_address='dfgh',
            user_email='sjk@gmail.com',
            date_of_birth=19 - 7 - 2000
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == "/login"


def test_profile_post(client):
    response = client.post(
        "/login",
        data=dict(
            user_name='steff',
            user_phone_number=1234567895,
            user_first_name='steff',
            user_last_name='jk',
            user_age=21,
            user_address='dfgh',
            user_email='sjk@gmail.com',
            date_of_birth=19 - 7 - 2000
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert response.request.path == "/login"


# need to log in for accessing this end point
def test_request_card(client):
    response = client.post(
        "/user/request-card",
        follow_redirects=True)
    assert response.status_code == 200
    assert "Please log in to access this page." in str(response.data)


# if card is already exist
def test_request_new_card(client, login):
    response = client.post(
        "/user/request-card",
        follow_redirects=True)
    assert response.status_code == 200
    assert 'You have already Card' in str(response.data)


# if card is not exist [ must have user account ]
def test_req_already_existed_card(client, login2):
    response = client.post(
        "/user/request-card",
        follow_redirects=True)
    assert response.status_code == 200
    assert 'your card has been created' in str(response.data)


# for loan
def test_loan(client, login):
    response = client.post(
        "/user/apply-for-loan",
        follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/user/apply-for-loan"


# already have loan
def test_already_loan_exist(client, login):
    response = client.post(
        "/user/apply-for-loan",
        data=dict(loan_amount_choices=1, loan_rate_interests=1, loan_type='Home loan'),
        follow_redirects=True)
    assert 'You have already current LOAN' in str(response.data)


# creating new loan req. [ recheck this one - duplication]
# def test_create_new_loan(client, login2):
#     response = client.post(
#         "/user/apply-for-loan",
#         data=dict(loan_amount_choices=1, loan_rate_interests=1, loan_type='data', add_loan_type=True),
#         follow_redirects=True)
#     assert response.status_code == 200
#     assert 'Your LOAN has been requested with inactive status' in str(response.data)

def test_get_req_loan(client, login):
    get_data = client.get(
        "/user/apply-for-loan",
        follow_redirects=True)
    assert '<input class="form-control form-control-lg" id="user_name" ' \
           'name="user_name" readonly type="text" value="steffy">' in str(get_data.data)
    assert '<input class="form-control form-control-lg" id="user_id" name="user_id" readonly type="text" value="1">' in str(
        get_data.data)


# for user 1 we created insurance1 so insurance already exist checked here
def test_already_insurance_exist(client, login):
    response = client.post(
        "/user/request-insurance",
        data=dict(insurance_amount_choices=1, insurance_type='Home insurance'),
        follow_redirects=True)
    assert 'You have already current Insurance' in str(response.data)


# creating new insurance req. [ recheck this one - duplication]
def test_create_new_insurance(client, login2):
    response = client.post(
        "/user/request-insurance",
        data=dict(insurance_amount_choices=1, insurance_type='Home insurance'),
        follow_redirects=True)
    assert response.status_code == 200
    assert 'Your Insurance has been requested with inactive status' in str(response.data)


# check request.get method is actually works in this route
def test_get_req_insurance(client, login):
    get_data = client.get(
        "/user/request-insurance",
        follow_redirects=True)
    assert '<input class="form-control form-control-lg" id="user_name" ' \
           'name="user_name" readonly type="text" value="steffy">' in str(get_data.data)
    assert '<input class="form-control form-control-lg" id="user_id" name="user_id" readonly type="text" value="1">' in str(
        get_data.data)


def test_change_branch(client, login):
    res = client.get("/user/change_branch",
                     follow_redirects=True)
    assert "Account status change" in str(res.data)
    assert res.status_code == 200


def test_get_profile(client, login):
    data = client.get("/profile", follow_redirects=True)
    assert data.status_code == 200


def test_get_transfer_money(client, login):
    data = client.get("/user/transfer-money", follow_redirects=True)
    assert data.status_code == 200


def test_get_otp_check(client, login):
    data = client.get("/user/otp-check", follow_redirects=True)
    assert data.status_code == 200


def test_logout(client, login):
    res = client.get("/user/logout", follow_redirects=True)
    assert res.status_code == 200
    assert 'Logout successfully..' in str(res.data)


def test_profile_post_data(client, login):
    res = client.post("/profile",
                      data=dict(
                          user_name='steff007', user_phone_number=1234567895,
                          user_first_name='steffy', user_last_name='jk',
                          user_address='nyx', user_age=21, date_of_birth=19 - 7 - 2000,
                      ),
                      follow_redirects=True)
    print("==========is is data: ", res.data)
    assert res.status_code == 200
    assert 'steff007' in str(res.data)
    assert '1234567895' in str(res.data)
    assert 'steffy' in str(res.data)
    assert 'jk' in str(res.data)
    assert 'nyx' in str(res.data)
    assert '21' in str(res.data)


def test_check_user_name_duplication(client, login):
    res = client.post("/profile",
                      data=dict(
                          user_name='stella', user_phone_number=1234595,
                          user_first_name='steffy', user_last_name='jk',
                          user_address='nyx', user_age=21, date_of_birth=19 - 7 - 2000,
                      ),
                      follow_redirects=True)
    assert 'That username is taken please Choose different one' in str(res.data)


def test_phone_number_validation(client, login):
    res = client.post("/profile",
                      data=dict(
                          user_name='stella', user_phone_number=1234595,
                          user_first_name='steffy', user_last_name='jk',
                          user_address='nyx', user_age=21, date_of_birth=19 - 7 - 2000,
                      ),
                      follow_redirects=True)
    assert 'Phone number must be 10 digits' in str(res.data)


def test_check_registration_validation(client):
    response = client.post("/user/registration",
                           data=dict(
                               user_id=7, user_name='steff', user_email='steff@gmail.com',
                               user_phone_number=12345678, user_first_name='steff',
                               user_last_name='steffjk', user_address='407,NYC',
                               user_age=21, date_of_birth=datetime.utcnow(),
                               user_password='steff@123', confirm_password='steff@',
                               role_assign=True, account_creation=True
                           ), follow_redirects=True
                           )
    assert response.status_code == 200
    assert 'The length must be 10 for the phone number' in str(response.data)
    assert 'Confirm passwd must be equal to paasword' in str(response.data)


def test_reset_pwd_email_exist_in_db(client):
    response = client.post("/reset_password", data=dict(user_email="sdfgh@gmail.com"), follow_redirects=True)
    assert response.status_code == 200
    assert 'There is no account with that email. YOu must register first! ' in str(response.data)


def test_money_rec_account_exist(client, login):
    res = client.post("/user/add-money-to-other", data=dict(reciver_account=56,
                                                            credit_amount=150, user_password='steffy@123'),
                      follow_redirects=True)
    assert res.status_code == 200
    assert 'No account is exist in this number' in str(res.data)
