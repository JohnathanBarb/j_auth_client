# j_auth_client


## Usage example

```python
from requests import post

from j_auth_client.client import JAuthClient


class MyClient(JAuthClient):
    def __init__(self, auth_username: str, auth_password: str, auth_url: str, routes: dict):
        super().__init__(auth_username, auth_password, auth_url)
        self.routes = routes
    
    def create_todo(self, todo: dict) -> dict:
        return self.request(
            method=post,
            url=self.routes["create_todo"],
            json=todo,
            auth_server_authenticated=True,
        )
```
