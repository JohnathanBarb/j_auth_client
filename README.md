# j_auth_client

A simple client for authenticating with a JAuth server.

Available on [PyPi](https://pypi.org/project/j-auth-client/).

### Usage example

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
        ).json()
```

### Contributing

This project is open to contributions. Please feel free to open an issue or a pull request.

#### UV
To run, build and publish this project we are using [UV](https://docs.astral.sh/uv/).
See Makefile for available and used commands.


#### pre-commit

This project uses [pre-commit](https://pre-commit.com/) to run some checks before committing.
We use pre-commit to enforce lint, formatting, commit messages and others.


After installed pre-commit, run the following command to install the hooks:
```bash
pre-commit install
```

Run all checks without committing:
```bash
pre-commit run -a
````
