from datetime import datetime

# registration successfully
def test_registration_post(client):
    response = client.post("/user/registration",
                           data=dict(user_id=55,
                                     user_name='demodata', user_email='vacationsfever2021@gmail.com',
                                     user_phone_number=1234567895, user_first_name='steff',
                                     user_last_name='steffjk', user_address='407,NYC',
                                     user_age=22,
                                     user_password='Steff@123', confirm_password='Steff@123',
                                     submit="Sign Up", role_assign=True,
                                     date_of_birth="2000-5-19")
                           , follow_redirects=True
                           )
    assert response.status_code == 200
    assert 'Your account has been created you are all set for login' in str(response.data)

# registration while empty field [ same for all field ]
def test_registration_empty_field(client):
    response = client.post("/user/registration",
                           data=dict(user_name='', user_email='vacationsfever2021@gmail.com',
                                     user_phone_number=1234567895, user_first_name='steff',
                                     user_last_name='steffjk', user_address='407,NYC',
                                     user_age=22,
                                     user_password='Steff@123', confirm_password='Steff@123',
                                     submit="Sign Up", role_assign=True,
                                     date_of_birth="2000-6-19")
                           , follow_redirects=True
                           )
    assert response.status_code == 200
    assert 'This field is required' in str(response.data)


# check validation for duplication in user_name while registration
def test_duplication_in_user_name_registration(client):
    response = client.post("/user/registration",
                           data=dict(
                               user_name='steffy', user_email='vacationsfever2021@gmail.com',
                               user_phone_number=1234567895, user_first_name='steff',
                               user_last_name='steffjk', user_address='407,NYC',
                               user_age=21, date_of_birth="2000-6-12",
                               user_password='steff@123', confirm_password='steff@123',
                               submit="Sign Up")
                           , follow_redirects=True
                           )
    assert response.status_code == 200
    assert 'That username is taken please Choose different one' in str(response.data)


# check validation for duplication in user_email while registration
def test_duplication_in_user_email_registration(client):
    response = client.post("/user/registration",
                           data=dict(
                               user_name='steffy', user_email='steffy.jk2018@gmail.com',
                               user_phone_number=1234567895, user_first_name='steff',
                               user_last_name='steffjk', user_address='407,NYC',
                               user_age=22, date_of_birth="2000-11-19",
                               user_password='steff@123', confirm_password='steff@123',
                               submit="Sign Up")
                           , follow_redirects=True
                           )
    assert response.status_code == 200
    assert 'That email is taken please Choose different one' in str(response.data)

#admin can also add user
def test_registration_with_admin(client, admin_login):
    response = client.post("/user/registration",
                           data=dict(
                               user_id=7, user_name='steff', user_email='steff@gmail.com',
                               user_phone_number=1234567894, user_first_name='steff',
                               user_last_name='steffjk', user_address='407,NYC',
                               user_age=22, date_of_birth="2000-6-12",
                               user_password='Steff@123', confirm_password='Steff@123',
                               role_assign=True, account_creation=True
                           ), follow_redirects=True
                           )

    assert 'steffy.inexture@gmail.com' in str(admin_login.data)
    assert 'New user added successfully' in str(response.data)

#succsessfull log in
def test_login(login):
    assert 'Login successfully' in str(login.data)
    assert login.status_code == 200
    assert login.request.path == "/user-dashboard"


# user tries to log in but the account is not activated by admin
def test_login_inactive_account(client):
    res = client.post("/login", data=dict(user_email='inactive.jk2018@gmail.com',
                                          user_password='inactive@123', remember="y"),
                      follow_redirects=True)
    assert 'Hey! admin does not activate your account yet! cant login rn' in str(res.data)


# password is not correct so login unsuccessfully
def test_login_unsuccessfull(client):
    res = client.post("/login", data=dict(user_email='steffy.jk2018@gmail.com',
                                          user_password='dfghj@123', remember="y"),
                      follow_redirects=True)
    assert 'Login unsuccessfully..please check email and password' in str(res.data)


# test wrong login data
def test_wrong_credentials(login_fake):
    assert 'Login unsuccessfully..please check email and password' in str(login_fake.data)
    assert login_fake.status_code == 200

# user dashboard's get request
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


def test_profile_post(client):
    response = client.post(
        "/profile",
        data=dict(
            user_id=1,
            user_name='steffyjk',
            user_phone_number=1234567895,
            user_first_name='steff',
            user_last_name='jk',
            user_age=21,
            user_address='dfgh',
            user_email='sjk@gmail.com',
            date_of_birth="2000-12-12"
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Your account has been update!' in str(response.data)


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


def test_profile_post_by_admin(client, admin_login):
    response = client.post(
        "/profile",
        data=dict(
            user_name='steff',
            user_email="steffy.inexture@gmail.com",
            user_phone_number=1234567895,
            user_first_name='steff',
            user_last_name='jk',
            user_age=21,
            user_address='dfgh',
            date_of_birth="2000-12-12"
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert 'Your account has been update!' in str(response.data)


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


def test_create_new_insurance_choice2(client, login2):
    response = client.post(
        "/user/request-insurance",
        data=dict(insurance_amount_choices=2, insurance_type='Home insurance'),
        follow_redirects=True)
    assert response.status_code == 200
    assert 'Your Insurance has been requested with inactive status' in str(response.data)


def test_create_new_insurance_choice_3(client, login2):
    response = client.post(
        "/user/request-insurance",
        data=dict(insurance_amount_choices=3, insurance_type='Home insurance'),
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


# check weather transfer amount > account balance for choice 1
def test_user_money_form_data(client, login):
    response = client.post("/user/transfer-money",
                           data=dict(user_id=1, user_name='steffy', transfer_choice='1',
                                     transfer_amount=5003, user_password='steffy@123', otp_btn=True,
                                     ),
                           follow_redirects=True)
    assert response.status_code == 200
    assert 'Insufficient balance' in str(response.data)


# check weather transfer amount > account balance for choice 4 [ fd ]
def test_user_money_form_data(client, login):
    response = client.post("/user/transfer-money",
                           data=dict(user_id=1, user_name='steffy', transfer_choice='4',
                                     transfer_amount=5003, user_password='steffy@123', otp_btn=True,
                                     ),
                           follow_redirects=True)
    assert response.status_code == 200
    assert 'Insufficient balance' in str(response.data)

# user has not applied for fd yet
def test_user_money_but_user_has_no_fd(client, login2):
    response = client.post("/user/transfer-money",
                           data=dict(user_id=2, user_name='stella', transfer_choice='4',
                                     transfer_amount=250, user_password='stella@123', otp_btn=True,
                                     ),
                           follow_redirects=True)
    assert response.status_code == 200
    assert 'you have not requested for fd yet' in str(response.data)


# user has fd but its inactive
def test_user_money_but_inactive_fd(client, login_user_nine_five):
    response = client.post("/user/transfer-money",
                           data=dict(user_id=95, user_name='loanuser', transfer_choice='4',
                                     transfer_amount=250, user_password='loanuser@123', otp_btn=True,
                                     ),
                           follow_redirects=True)
    assert response.status_code == 200
    assert 'Fd status needs to activate first' in str(response.data)


# reset password info request
def test_reset_req(client):
    response = client.post("/reset_password",
                           data=dict(user_email="steffy.jk2018@gmail.com"),
                           follow_redirects=True)
    assert 'An email has been sent with instruction to reset your password.' in str(response.data)


def test_reset_req_get(client, login):
    response = client.post("/reset_password",
                           follow_redirects=True)
    assert response.status_code == 200


def test_bank_statement(client, login):
    response = client.post("/user/bank-statement/", follow_redirects=True)
    assert response.status_code == 200


# change the branch by the user
# case-1 branch is existed
def test_change_account_branch(client, login):
    response = client.post("/user/change_branch",
                           data=dict(user_id=1, user_name="steffy", account_number=1000000,
                                     myField="test branch"), follow_redirects=True)
    assert response.status_code == 200
    assert 'Bank branch has been updated/changed' in str(response.data)


# case-2 branch is not existed throwing error
def test_branch_is_not_existed(client, login):
    response = client.post("/user/change_branch",
                           data=dict(user_id=1, user_name="steffy", account_number=1000000,
                                     myField="test d"), follow_redirects=True)
    assert response.status_code == 200
    assert 'There is some error' in str(response.data)


# for applying fixed deposit by user side

# case-1 user already have fixed deposit
def test_add_fd_but_user_already_have_fd(client, login):
    response = client.get("/user/add_fixed_deposit", follow_redirects=True)
    assert 'You have already current {activity}'.format(activity="FIXED DEPOSIT") in str(response.data)


# case-2 user has applied for fd for the first time [ so successfully apply for fd ]
def test_add_fd_but_user_apply_for_first_time(client, login2):
    response = client.get("/user/add_fixed_deposit", follow_redirects=True)
    assert 'Your {activity} has been requested with inactive status'.format(activity="FIXED DEPOSIT") in str(
        response.data)


# for applying the loan requests
# case 1 choose 1st option
def test_apply_loan_with_first(client, login_user_nine_five):
    response = client.post("/user/apply-for-loan",
                           data=dict(user_id=95, user_name="loanuser", loan_amount_choices=1,
                                     loan_rate_interests=1, loan_type="Home loan"),
                           follow_redirects=True)
    assert 'Your {activity} has been requested with inactive status'.format(activity="loan") in str(response.data)


# case 1 choose 2st option
def test_apply_loan_with_second(client, login_user_nine_five):
    response = client.post("/user/apply-for-loan",
                           data=dict(user_id=95, user_name="loanuser", loan_amount_choices=2,
                                     loan_rate_interests=2, loan_type="Home loan"),
                           follow_redirects=True)
    assert 'Your {activity} has been requested with inactive status'.format(activity="loan") in str(response.data)


# case 1 choose 3rd option
def test_apply_loan_with(client, login_user_nine_five):
    response = client.post("/user/apply-for-loan",
                           data=dict(user_id=95, user_name="loanuser", loan_amount_choices=3,
                                     loan_rate_interests=1, loan_type="Home loan"),
                           follow_redirects=True)
    assert 'Your {activity} has been requested with inactive status'.format(activity="loan") in str(response.data)


# money transaction
# case-1 to someone else account
def test_money_success_to_someone_acc(client, login):
    res = client.post("/user/add-money-to-other",
                      data=dict(reciver_account=1000001, credit_amount=100, user_password="steffy@123"),
                      follow_redirects=True)
    assert "Transaction is successfully done" in str(res.data)


# case-2 to account itself
def test_money_success_to_same_acc(client, login):
    res = client.post("/user/add-money-to-other",
                      data=dict(reciver_account=1000000, credit_amount=100, user_password="steffy@123"),
                      follow_redirects=True)
    assert 'You can not transfer to yourself it does not make any sense' in str(res.data)


# case-3 insufficient balance
def test_money_but_insufficient_balance(client, login):
    res = client.post("/user/add-money-to-other",
                      data=dict(reciver_account=1000001, credit_amount=5040, user_password="steffy@123"),
                      follow_redirects=True)
    assert 'Insufficient balance you have only:5000' in str(res.data)

# case4 incorrect password
def test_money_but_incorrect_pwd(client, login):
    res = client.post("/user/add-money-to-other",
                      data=dict(reciver_account=1000001, credit_amount=250, user_password="65@123"),
                      follow_redirects=True)
    assert 'Password is incorrect' in str(res.data)