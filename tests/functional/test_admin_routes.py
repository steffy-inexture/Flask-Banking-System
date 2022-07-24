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
def test_fd_status_change_but_account_not_found(client, admin_login):
    response = client.post("/admin/update-fd-status/3/",
                           data=dict(user_id=3, user_name="admin", ),
                           follow_redirects=True)
    assert "No {activity} records found for this user".format(activity='Account') in str(response.data)


# change the fd status by the admin but user is not exist
def test_fd_status_change_but_user_not_found(client, admin_login):
    response = client.post("/admin/update-fd-status/60/",
                           data=dict(user_id=60, user_name="fat", ),
                           follow_redirects=True)
    assert "No user found in this user id {id}".format(id='60') in str(response.data)


# for fd approval use and account exist but user is not applied for any fd
def test_fd_is_not_exist(client, admin_login):
    response = client.post("/admin/update-fd-status/2/", data=dict(user_id=2),
                           follow_redirects=True)
    assert "No {activity} records found for this user".format(activity="Fixed deposit") in str(response.data)


# delete fd for particular user
def test_delete_fd_data(client, admin_login):
    response = client.post("/admin/delete-fd/1/", data=dict(user_id=1),
                           follow_redirects=True)
    assert "1 this is the name" in str(response.data)


# for account changing option

# case-1 user not exist validation
def test_user_not_exist_in_account_change(client, admin_login):
    response = client.post("/admin/change-account-status/65/", data=dict(user_id=65),
                           follow_redirects=True)
    assert "No user found in this user id {id}".format(id='65') in str(response.data)


# case-2 user exist but user has no account
def test_account_status_change_but_account_not_found(client, admin_login):
    response = client.post("/admin/change-account-status/3/",
                           data=dict(user_id=3, user_name="admin", ),
                           follow_redirects=True)
    assert "No {activity} records found for this user".format(activity='Account') in str(response.data)


# case-3 admin activate the status successfully
def test_change_to_active_status(client, admin_login):
    respopnse = client.post("/admin/change-account-status/1/",
                            data=dict(user_id=1, user_name="steffy",
                                      account_number=1000000, account_status="1"),
                            follow_redirects=True)
    assert "{user_name}s Account status has been changed :)".format(user_name="steffy") in str(respopnse.data)


# case-4 admin Inactive the status successfully
def test_change_to_inactive_status(client, admin_login):
    response = client.post("/admin/change-account-status/1/",
                           data=dict(user_id=1, user_name="steffy",
                                     account_number=1000000, account_status="2"),
                           follow_redirects=True)
    assert "{user_name}s Account status has been changed :)".format(user_name="steffy") in str(response.data)


# testing add branch option by admin side
# case 1 branch data is already exist in database
def test_add_branch_existed(client, admin_login):
    response = client.post("/admin/add-branch/",
                           data=dict(branch_name="test branch", branch_address="test b-address"),
                           follow_redirects=True)
    assert 'This branch has already exist!' in str(response.data)


# case 2 branch added successfully without duplication
def test_add_branch_successfully(client, admin_login):
    response = client.post("/admin/add-branch",
                           data=dict(branch_name="Ney york", branch_address="NYC"),
                           follow_redirects=True)
    assert 'Branch is added successfully' in str(response.data)


# testing add atm option by admin side
# case 1 atm data is already exist in database
def test_add_atm_existed(client, admin_login):
    response = client.post("/admin/add-atm/",
                           data=dict(atm_address='ahmedabad'),
                           follow_redirects=True)
    assert 'Atm has already exist at this area!' in str(response.data)


# case 2 atm added successfully without duplication
def test_add_atm_successfully(client, admin_login):
    response = client.post("/admin/add-atm",
                           data=dict(atm_address="New york"),
                           follow_redirects=True)
    assert 'Atm is added successfully' in str(response.data)


# check to delete bank member
def test_delete_bank_member(client, admin_login):
    response = client.post("/admin/delete-bank-member/1/",
                           data=dict(member_id=1),
                           follow_redirects=True)
    assert "Bank member has been deleted" in str(response.data)


# for deleting the bank member role from the member role list
# case-1 member role is occupied
def test_delete_occupied_member_role(client, admin_login):
    res = client.post("/admin/delete-member-role-from-list/7", data=dict(id=7), follow_redirects=True)
    assert "This role is occupied by some bank member you can not delete that." in str(res.data)


# case-1 member role is not occupied so deleted successfully
def test_delete_unoccupied_member_role(client, admin_login):
    res = client.post("/admin/delete-member-role-from-list/8", data=dict(id=8), follow_redirects=True)
    assert "Desired role deleted successfully" in str(res.data)


# testing add bank role option by admin side
# case 1 add bank role is already exist in database
def test_bank_role_already_exist(client, admin_login):
    response = client.post("/admin/add-bank-role/",
                           data=dict(role_name='CEO'),
                           follow_redirects=True)
    assert "This role is already exist" in str(response.data)


# case 2 bank role added successfully without duplication
def test_bank_role_added_successfully(client, admin_login):
    response = client.post("/admin/add-bank-role/",
                           data=dict(role_name="Accountant"),
                           follow_redirects=True)
    assert "New role has been added" in str(response.data)


def test_add_bank_role(client, admin_login):
    response = client.get("/admin/add-bank-role/",
                          follow_redirects=True)
    assert response.status_code == 200


# testing add loan choice option by admin side
# case 1 add loan choice is already exist in database
def test_loan_choice_already_exist(client, admin_login):
    response = client.post("/admin/add-loan-options/",
                           data=dict(loan_choice='Home loan'),
                           follow_redirects=True)
    assert "This loan choice is already exist" in str(response.data)


# case 2 bank loan choice added successfully without duplication
def test_loan_choice_added_successfully(client, admin_login):
    response = client.post("/admin/add-loan-options/",
                           data=dict(loan_choice='Phone loan'),
                           follow_redirects=True)
    assert "New loan Choice has been added" in str(response.data)


def test_add_loan_choice(client, admin_login):
    response = client.get("/admin/add-loan-options/",
                          follow_redirects=True)
    assert response.status_code == 200


# delete loan option choice

# case-1 loan choice option is occupied by the user loan
def test_delete__occupied_loan_choice(client, admin_login):
    response = client.post("/admin/delete-loan-options/11",
                           follow_redirects=True)

    assert "Loan choice is occupied with some user you can not delete this" in str(response.data)


# case-2 loan choice is successfully deleted as its not occupied so admin can delete that
def test_delete_loan_choice_successfully(client, admin_login):
    response = client.post("/admin/delete-loan-options/12",
                           follow_redirects=True)

    assert "Desired Loan choice has been deleted from the list successfully" in str(response.data)


# testing status code
def test_get_delete_loan_choice(client, admin_login):
    response = client.post("/admin/delete-loan-options/12",
                           follow_redirects=True)

    assert response.status_code == 200


# delete insurance option choice

# case-1 insurance choice option is occupied by the user insurance
def test_delete_occupied_insurance_choice(client, admin_login):
    response = client.post("/admin/delete-insurance-options/13",
                           follow_redirects=True)

    assert "Insurance choice is occupied with some user you can not delete this" in str(response.data)


# case-2 insurance choice is successfully deleted as its not occupied so admin can delete that
def test_delete_insurance_choice_successfully(client, admin_login):
    response = client.post("/admin/delete-insurance-options/14",
                           follow_redirects=True)

    assert "Desired Insurance choice has been deleted from the list successfully" in str(response.data)


# testing status code
def test_get_delete_insurance_choice(client, admin_login):
    response = client.get("/admin/delete-insurance-options/14",
                          follow_redirects=True)

    assert response.status_code == 200

# testing add insurance choice option by admin side
# case 1 add insurance choice is already exist in database
def test_insurance_choice_already_exist(client, admin_login):
    response = client.post("/admin/add-insurance-options/",
                           data=dict(insurance_choice='Life insurance'),
                           follow_redirects=True)
    assert "This insurance is already exist" in str(response.data)


# case 2 bank insurance choice added successfully without duplication
def test_insurance_choice_added_successfully(client, admin_login):
    response = client.post("/admin/add-insurance-options/",
                           data=dict(insurance_choice='Phone insurance'),
                           follow_redirects=True)
    assert "New insurance detail has been added" in str(response.data)


def test_add_insurance_choice(client, admin_login):
    response = client.get("/admin/add-insurance-options/",
                          follow_redirects=True)
    assert response.status_code == 200
