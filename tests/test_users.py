from app import schema
from app import schema
from app import oauth2
from app.config import settings

def test_create_user(client):
    res = client.post("/users/", json={
        "email": "obodochibueze1234@gmail.com", "password":"Chibueze2007"
    })
    new_user = schema.UserResponse(**res.json())
    assert new_user.email == "obodochibueze1234@gmail.com"
    assert res.status_code == 201
    
def test_login(client, test_user):
    res = client.post("/login", json={
        "email": test_user["email"], "password": test_user["password"]
    })
    token_data = schema.UserTokenResponse(**res.json())
    payload = oauth2.jwt.decode(token_data.access_token, settings.SECRET_KEY, settings.ALGORITHM)
    id = payload.get("user_id")
    assert id == test_user['id']
    assert res.status_code == 200