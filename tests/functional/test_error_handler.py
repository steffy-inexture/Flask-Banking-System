def test_403(client,login):
    response = client.get("/admin/change-account-status/520/?user_name=demo4&account_number=1000000",follow_redirects=True)
    assert 'only admin can has the access of that previous page' in str(response.data)

def test_404(client,admin_login):
    response = client.get("/insurancefvghj",follow_redirects=True)
    assert '(ERROR 404)' in str(response.data)

