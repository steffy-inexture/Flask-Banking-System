def test_get_loan_approval(client,admin_login):
    data = client.get("/admin/loan-approval-status/<1>/",follow_redirects=True)
    assert data.status_code == 200

def test_get_insurance_approval(client,admin_login):
    data = client.get("/admin/insurance-approval-status/<1>/",follow_redirects=True)
    assert data.status_code == 200

def test_get_update_fd_status(client,admin_login):
    data = client.get("/admin/update-fd-status/<user_id>/",follow_redirects=True)
    assert data.status_code == 200

def test_get_change_account_status(client,admin_login):
    data = client.get("/admin/change-account-status/<user_id>/",follow_redirects=True)
    assert data.status_code == 200

def test_get_bank_member(client,admin_login):
    data = client.get("/admin/bank-about-member/",follow_redirects=True)
    assert data.status_code == 200
