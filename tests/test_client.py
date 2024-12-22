from j_auth_client.client import JAuthClient


def test_client():
    client = JAuthClient(
        username="username",
        password="password",
        auth_url="https://auth.example.com",
    )

    assert client.token is None
    assert client.token_expires_at is None
    assert client.username == "username"
    assert client.password == "password"
    assert client.auth_url == "https://auth.example.com"
