from fastapi.testclient import TestClient
from add import app

client = TestClient(app)

#testhomeapi
def test_home():
    response = client.get("/")
    #status code check
    assert response.status_code == 200
    #response data check
    assert response.json() == {"msg":"hello bits"}

#test add api
def test_add():
    response = client.get("/add?a=5&b=7")

    assert response.status_code == 200
    assert response.json() == {"result":12}