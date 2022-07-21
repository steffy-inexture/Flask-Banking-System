from datetime import datetime


def test_registration(client):
    response = client.post("/user/registration",
                           data=dict(
                               user_id=7,
                               user_name='steff',
                               user_email='steff@gmail.com',
                               user_phone_number=1234567894,
                               user_first_name='steff',
                               user_last_name='steffjk',
                               user_address='407,NYC',
                               user_age=21,
                               date_of_birth=datetime.utcnow(),
                               user_password='steff@123',
                               confirm_password='steff@123',
                           ),
                           )
    assert response.status_code == 200


def test_login(login):
    assert 'Login successfully' in str(login.data)
    assert login.status_code == 200
    assert login.request.path == "/user-dashboard"

#test wrong login data
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


