def test_money_page(client,admin_login):
    response = client.get("/money",follow_redirects=True)
    assert 'About money' in str(response.data)

def test_fixed_deposits(client,admin_login):
    response = client.get("/fixed-deposits",follow_redirects=True)
    assert 'About fixed deposits' in str(response.data)

def test_loan(client,admin_login):
    response = client.get("/loan",follow_redirects=True)
    assert 'About loan' in str(response.data)

def test_insurance_page(client,admin_login):
    response = client.get("/insurance",follow_redirects=True)
    assert 'About insurance' in str(response.data)