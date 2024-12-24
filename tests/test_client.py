import unittest

from requests import get

from j_auth_client.client import JAuthClient


class TestJAuthClient(unittest.TestCase):
    def setUp(self):
        self.auth_username = "username"
        self.auth_password = "password"
        self.auth_url = "https://auth.example.com"

        self.j_auth_client_instance = JAuthClient(
            auth_username=self.auth_username,
            auth_password=self.auth_password,
            auth_url=self.auth_url,
        )

    def test_client(self):
        assert self.j_auth_client_instance.token is None
        assert self.j_auth_client_instance.token_expires_at is None
        assert self.j_auth_client_instance.auth_username == self.auth_username
        assert self.j_auth_client_instance.auth_password == self.auth_password
        assert self.j_auth_client_instance.auth_url == self.auth_url

    def test_request_without_authentication(self):
        response = self.j_auth_client_instance.request(
            method=get,
            url="https://httpbin.org/anything",
            auth_server_authenticated=False,
        )

        assert response.status_code == 200
        assert isinstance(response.json(), dict)
