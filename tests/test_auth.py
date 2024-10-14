from conftest import client



def test_register():
    response = client.post("/auth/register", json={
        "email": "string@test.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "String"
    })

    assert response.status_code == 201