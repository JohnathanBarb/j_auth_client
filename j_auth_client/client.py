from datetime import datetime
from typing import Any, Dict, Optional

from requests import post, request
from jwt import decode
from requests.auth import HTTPBasicAuth


class JAuthClient:
    token: str = None
    token_expires_at: datetime = None

    def __init__(
        self,
        username: str,
        password: str,
        auth_url: str,
    ):
        self.username = username
        self.password = password
        self.auth_url = auth_url

    def __authenticate(self):
        response = self.request(
            method=post,
            url=self.auth_url,
            data={"grant_type": "client_credentials"},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=HTTPBasicAuth(self.username, self.password),
            auth_server_authenticated=False,
        )

        self.token = response["access_token"]
        self.token_expires_at = datetime.fromtimestamp(
            int(decode(jwt=self.token, options={"verify_signature": False})["exp"])
        )

    @property
    def __should_authenticate(self):
        return not self.token or self.token_expires_at < datetime.now()

    def request(
        self,
        method: request,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        auth: Optional[HTTPBasicAuth] = None,
        auth_server_authenticated: Optional[bool] = True,
    ) -> dict:
        json = json or {}
        headers = headers or {}
        data = data or {}

        if auth_server_authenticated and self.__should_authenticate:
            self.__authenticate()
            headers["Authorization"] = f"Bearer {self.token}"

        response = method(url=url, headers=headers, json=json, data=data, auth=auth)
        response.raise_for_status()

        return response.json()
