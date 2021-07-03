# Authenticator middleware for Python Falcon

Python [Falcon](https://falcon.readthedocs.io/en/stable/) is a great, lightweight and fast Python framework to create
HTTP APIs. This package provides an easy add-on to configure a middleware for authentication.

## Usage
```python
import falcon
from python_falcon_authenticator import PythonFalconAuthenticator
from python_falcon_authenticator.authenticators.jwt import Authenticator as JwtAuthenticator
from python_falcon_authenticator.decorators import resource_auth_config
from python_falcon_authenticator.utils.route_requests_with_responder import RouterWithRequestResponder

authenticator = PythonFalconAuthenticator(
    JwtAuthenticator(
        client_id="CliEnTiD",
        oauth_api="https://oauth.auth.com",
    )
)


@resource_auth_config(
    skip_methods=['POST'],  # skip a given method
    skip_uris=['/users'],  # skip a given uri TEMPLATE used in add_route())
    skip_responders=['on_post']  # skip a responder name
)
class UsersResource:
    def on_post(self, req, resp):
        # The authorization of this endpoint is skipped because of the
        # three skip conditions
        resp.media = {"hello": "world"}

    def on_get(self, req, resp):
        # This one is skipped only because of skip_uris
        resp.media = {"hello": "world"}


api = falcon.API(
    middleware=[authenticator],
    router=RouterWithRequestResponder())

api.add_route("/users", UsersResource())
```

## Authorizers

#### OpenID JWT
> requirements:
> * [cryptography](https://pypi.org/project/cryptography/)
> * [jwt](https://pypi.org/project/jwt/)
> * requests

#### Static Basic
Statically provide username and password to match
```py
from python_falcon_authenticator.authenticators.static_basic import Authenticator as BasicAuthenticator

authenticator = BasicAuthenticator(
    username="raphaeljoie",
    password="Passw0rd"
)
```
