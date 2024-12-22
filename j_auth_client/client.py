from datetime import datetime
from typing import Any, Dict, Optional

from requests import post, request


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
        )

        self.token = response["access_token"]
        self.token_expires_at = datetime.fromisoformat(response["expires_at"])

    @property
    def __should_authenticate(self):
        return not self.token or self.token_expires_at < datetime.now()

    def request(
        self,
        method: request,
        url: str,
        headers: Optional[Dict[str, Any]] = None,
        auth_server_authenticated: Optional[bool] = False,
    ) -> dict:
        if not headers:
            headers = {}

        if auth_server_authenticated and self.__should_authenticate:
            self.__authenticate()

        return method(url=url, headers=headers).json()
