def test_get_loan_approval(client, admin_login):
    data = client.get("/admin/loan-approval-status/1/", follow_redirects=True)
    assert data.status_code == 200


def test_get_insurance_approval(client, admin_login):
    data = client.get("/admin/insurance-approval-status/1/", follow_redirects=True)
    assert data.status_code == 200


def test_get_update_fd_status(client, admin_login):
    data = client.get("/admin/update-fd-status/1/", follow_redirects=True)
    assert data.status_code == 200


def test_get_change_account_status(client, admin_login):
    data = client.get("/admin/change-account-status/1/", follow_redirects=True)
    assert data.status_code == 200


def test_get_bank_member(client, admin_login):
    data = client.get("/admin/bank-about-member/", follow_redirects=True)
    assert data.status_code == 200


def test_admin_login(client):
    response = client.post("/admin_login", data=dict(user_id=5, user_email='steffy_inexture@gmail.com',
                                                     user_password='admin@123', remember="y"), follow_redirects=True)
    assert 'Admin Login successfully..' in str(response.data)


def test_admin_login_creditential(client):
    response = client.post("/admin_login", data=dict(user_id=5, user_email='steffy_inexture@gmail.com',
                                                     user_password='steff@123', remember="y"), follow_redirects=True)
    assert 'Login unsuccessfully..please check email and password' in str(response.data)
    assert response.status_code == 200


# checks the admin_user_data routes
def test_admin_user_data(client, admin_login):
    response = client.get("/all-user-data/", follow_redirects=True)
    assert response.status_code == 200


def test_delete_user_by_admin(client, admin_login):
    response = client.get("/admin/delete-user/2/", data=dict(user_id=2), follow_redirects=True)
    assert response.status_code == 200
    assert 'User is been deleted from the user :)' in str(response.data)


def test_admin_all_branch_data(client, admin_login):
    response = client.get("/admin/all-branch-data/", follow_redirects=True)
    assert response.status_code == 200


def test_admin_all_atm_data(client, admin_login):
    response = client.get("/admin/all-atm-data/", follow_redirects=True)
    assert response.status_code == 200


def test_admin_all_loan_data(client, admin_login):
    response = client.get("/admin/all-loan-data/", follow_redirects=True)
    assert response.status_code == 200


def test_admin_all_insurance_data(client, admin_login):
    response = client.get("/admin/all-insurance-data/", follow_redirects=True)
    assert response.status_code == 200


def test_admin_all_fd_data(client, admin_login):
    response = client.get("/admin/all-fd-data/", follow_redirects=True)
    assert response.status_code == 200


def test_bank_show_all_bank_member_data(client, admin_login):
    response = client.get("/admin/bank-show-all-member/", follow_redirects=True)
    assert response.status_code == 200


def test_show_member_role_list(client, admin_login):
    response = client.get("/admin/show_member_role_list", follow_redirects=True)
    assert response.status_code == 200


def test_show_loan_choice_list(client, admin_login):
    response = client.get("/admin/show_loan_choices/", follow_redirects=True)
    assert response.status_code == 200


def test_show_insurance_choices(client, admin_login):
    response = client.get("/admin/show_insurance_choices/", follow_redirects=True)
    assert response.status_code == 200


def test_delete_role(client, admin_login):
    response = client.get("/delete", follow_redirects=True)
    assert response.status_code == 200


def test_delete_branch_which_not_associated(client, admin_login):
    response = client.get("/admin/delete-branch-data/2", data=dict(branch_id=2), follow_redirects=True)
    assert response.status_code == 200
    assert 'Branch deleted Successfully' in str(response.data)


def test_delete_branch(client, admin_login):
    response = client.get("/admin/delete-branch-data/1", data=dict(branch_id=1), follow_redirects=True)
    assert response.status_code == 200
    assert 'This branch is interlinked with some account so you can not delete this branch' in str(response.data)


def test_delete_atm(client, admin_login):
    response = client.get("/admin/delete-atm-data/1", data=dict(atm_id=1), follow_redirects=True)
    assert response.status_code == 200
    assert 'Atm deleted successfully.' in str(response.data)


# for checking loan approval starts
def test_loan_approval_but_no_user_loan_found(client, admin_login):
    response = client.get("/admin/loan-approval-status/2/", data=dict(user_id=2), follow_redirects=True)
    assert response.status_code == 200
    assert "No Loan records found for this user" in str(response.data)


def test_admin_choose_to_active_user_loan(client, admin_login):
    response = client.post("/admin/loan-approval-status/1/", data=dict(user_id=1, approval_status="1",
                                                                       user_name="steffy", loan_id=1,
                                                                       loan_amount=5000, rate_interest=5.6,
                                                                       paid_amount=0, loan_type="personal loan",
                                                                       loan_status="Active"), follow_redirects=True)
    assert response.status_code == 200
    assert '{user_name}s {activity} status has been changed :)'.format(user_name='steffy', activity='loan') in str(
        response.data)


def test_admin_choose_to_inactive_user_loan(client, admin_login):
    response = client.post("/admin/loan-approval-status/1/", data=dict(user_id=1, approval_status="2",
                                                                       user_name="steffy", loan_id=1,
                                                                       loan_amount=5000, rate_interest=5.6,
                                                                       paid_amount=0, loan_type="personal loan",
                                                                       loan_status="Active"), follow_redirects=True)
    assert response.status_code == 200
    assert '{user_name}s {activity} status has been changed :)'.format(user_name='steffy', activity='loan') in str(
        response.data)


# check get request for loan approval
def test_check_get_for_loan_approval(client, admin_login):
    response = client.get("/admin/loan-approval-status/1/", follow_redirects=True)
    assert response.status_code == 200


# check weather user exist or not for loan approval
def test_user_exist_for_loan(client, admin_login):
    response = client.get("/admin/loan-approval-status/6/", follow_redirects=True)
    assert response.status_code == 200
    assert "No user found in this user id {id}".format(id=6) in str(response.data)


# for checking loan approval starts
def test_insurance_approval_but_no_user_loan_found(client, admin_login):
    response = client.get("/admin/insurance-approval-status/2/", data=dict(user_id=2), follow_redirects=True)
    assert response.status_code == 200
    assert "No Insurance records found for this user" in str(response.data)


# check get request for insurance approval
def test_check_get_for_insurance_approval(client, admin_login):
    response = client.get("/admin/insurance-approval-status/1/", follow_redirects=True)
    assert response.status_code == 200


# admin approving the insurance request
def test_admin_approve_insurance(client, admin_login):
    response = client.post("/admin/insurance-approval-status/1/", data=dict(user_id=1, approval_status="1",
                                                                            user_name="steffy", insurance_id=1,
                                                                            insurance_amount=5000,
                                                                            insurance_type="personal loan",
                                                                            insurance_status="Active"),
                           follow_redirects=True)
    assert response.status_code == 200
    assert '{user_name}s {activity} status has been changed :)'.format(user_name='steffy', activity='insurance') in str(
        response.data)


# admin declining the insurance request
def test_admin_decline_insurance(client, admin_login):
    response = client.post("/admin/insurance-approval-status/1/", data=dict(user_id=1, approval_status="2",
                                                                            user_name="steffy", insurance_id=1,
                                                                            insurance_amount=5000,
                                                                            insurance_type="personal loan",
                                                                            insurance_status="Active"),
                           follow_redirects=True)
    assert response.status_code == 200
    assert '{user_name}s {activity} status has been changed :)'.format(user_name='steffy', activity='insurance') in str(
        response.data)


# check weather user exist or not for insurance approval
def test_user_exist_for_insurance(client, admin_login):
    response = client.get("/admin/insurance-approval-status/6/", follow_redirects=True)
    assert response.status_code == 200
    assert "No user found in this user id {id}".format(id=6) in str(response.data)


# check get request for change the account status
def test_get_for_change_account_status(client, admin_login):
    response = client.get("/admin/change-account-status/1/", follow_redirects=True)
    assert response.status_code == 200


# for fd data updation from admin side
def test_fd_status_change(client, admin_login):
    response = client.get("/admin/update-fd-status/1/",
                          data=dict(user_id=1, user_name="steffy",
                                    fd_amount=1000, fd_status="1", fd_id=1),
                          follow_redirects=True)
    assert response.status_code == 200


# change the fd status by the admin "Active" [ user1 ]
def test_fd_status_change_post(client, admin_login):
    response = client.post("/admin/update-fd-status/1/",
                           data=dict(user_id=1, fd_id=1, user_name="steffy",
                                     fd_amount=5000, fd_status="Active"),
                           follow_redirects=True)
    assert '{user_name}s {activity} status has been changed :)'.format(user_name='steffy', activity='Fd') in str(
        response.data)


# change the fd status by the admin but user has no apply for fd [ user 2 ]
def test_fd_status_change_but_fd_not_found(client, admin_login):
    response = client.post("/admin/update-fd-status/2/",
                           data=dict(user_id=2, user_name="stella", ),
                           follow_redirects=True)
    assert "No {activity} records found for this user".format(activity='Fixed deposit') in str(
        response.data)


# change the fd status by the admin but user has no account information [ ex:admin ]
def test_fd_status_change_but_fd_not_found(client, admin_login):
    response = client.post("/admin/update-fd-status/3/",
                           data=dict(user_id=3, user_name="admin", ),
                           follow_redirects=True)
    assert "No {activity} records found for this user".format(activity='Account') in str(
        response.data)


# change the fd status by the admin but user is not exist
def test_fd_status_change_but_user_not_found(client, admin_login):
    response = client.post("/admin/update-fd-status/60/",
                           data=dict(user_id=60, user_name="fat", ),
                           follow_redirects=True)
    assert "No user found in this user id {id}".format(id='60') in str(response.data)

# delete fd for particular user
# def test_delete_fd_data(client,admin_login):
#     response = client.post("/admin/delete-fd/65/",data=dict(user_id=65),
#                            follow_redirects=True)
#     assert "No user found in this user id {id}".format(id='60') in str(response.data)
