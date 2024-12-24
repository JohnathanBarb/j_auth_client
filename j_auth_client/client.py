from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from jwt import decode
from requests import (
    ConnectionError,
    HTTPError,
    RequestException,
    Response,
    Timeout,
    post,
    request,
)
from requests.auth import HTTPBasicAuth

from j_auth_client.exceptions import (
    JAuthAuthenticationException,
    JAuthBaseException,
    JAuthClientException,
    JAuthConnectionException,
    JAuthRequestException,
    JAuthServerException,
    JAuthTimeoutException,
)


class JAuthClient:
    token: str = None
    token_expires_at: datetime = None

    def __init__(
        self,
        auth_username: str,
        auth_password: str,
        auth_url: str,
    ):
        """
        :param auth_username: username to authenticate on auth server
        :param auth_password: password to authenticate on auth server
        :param auth_url: url of auth server
        """

        self.auth_username = auth_username
        self.auth_password = auth_password
        self.auth_url = auth_url

    def __authenticate(self) -> None:
        """
        Authenticate request to get the token on defined auth server using client credentials
        refresh the token and expires_at on the instance

        :raises JAuthAuthenticationException:
        """
        try:
            response = self.request(
                method=post,
                url=self.auth_url,
                data={"grant_type": "client_credentials"},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                auth=HTTPBasicAuth(self.auth_username, self.auth_password),
                auth_server_authenticated=False,
            )

            self.token = response.json()["access_token"]
            self.token_expires_at = datetime.fromtimestamp(
                int(decode(jwt=self.token, options={"verify_signature": False})["exp"])
            )

        except (JAuthClientException, JAuthServerException) as error:
            raise JAuthAuthenticationException(
                message=f"Error on authentication request: {error.status_code} - {error.message} ",
            )

        except JAuthBaseException as error:
            raise JAuthAuthenticationException(
                message=f"Error on authentication request: {error.message}",
            )

    @property
    def __should_authenticate(self) -> bool:
        """Check if the token is expired or not set
        :return: bool
        """

        return not self.token or self.token_expires_at < (
            datetime.now() - timedelta(minutes=1)
        )

    def request(
        self,
        method: request,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        auth: Optional[HTTPBasicAuth] = None,
        auth_server_authenticated: Optional[bool] = True,
    ) -> Response:
        """
        Make a request to the defined url using or not the token from an auth server to authenticate

        :param method: request method
        :param url: request url
        :param json: (optional) request json as dict
        :param headers: (optional) request headers as dict
        :param data: (optional) request data as dict
        :param auth: (optional) HTTPBasicAuth if needed
        :param auth_server_authenticated: (optional) bool to authenticate or not on auth server

        :raises JAuthClientException: if the response status code is between 400 and 499
        :raises JAuthServerException: if the response status code is 500 or more
        :raises JAuthConnectionException: if a connection error occurs
        :raises JAuthTimeoutException: if a timeout error occurs
        :raises JAuthRequestException: if a request error occurs

        :return: Response (requests)
        """

        json = json or {}
        headers = headers or {}
        data = data or {}

        if auth_server_authenticated and self.__should_authenticate:
            self.__authenticate()
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            response = method(url=url, headers=headers, json=json, data=data, auth=auth)
            response.raise_for_status()
            return response

        except HTTPError as error:
            if 400 <= error.response.status_code < 500:
                raise JAuthClientException(
                    message=error.response.text,
                    status_code=error.response.status_code,
                )

            if error.response.status_code >= 500:
                raise JAuthServerException(
                    message=error.response.text,
                    status_code=error.response.status_code,
                )

        except ConnectionError as error:
            raise JAuthConnectionException(
                message=f"Error on connection: {error}",
            )

        except Timeout as error:
            raise JAuthTimeoutException(
                message=f"Timeout on request: {error}",
            )

        except RequestException as error:
            raise JAuthRequestException(
                message=f"Error on request: {error}",
            )
