def test_home_page(client):
    response = client.get("/home", follow_redirects=True)
    assert 'Hey! Welcome to the SJK banking system' in str(response.data)

def test_about_page(client):
    response = client.get("/about", follow_redirects=True)
    assert '<h1 style=" color:white ;">About Us Page</h1>' in str(response.data)