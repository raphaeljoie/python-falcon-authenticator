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
        oauth_domain="https://oauth.auth.com",
    )
)


class SecuredResource:
    def on_get(self, req, resp):
        # The request context is filled with authenticated user info
        # using a context builder function
        resp.media = {'calling_user_id': req.context.user_id}


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
api.add_route("/secured", SecuredResource())
```

## Authorizers

#### OpenID JWT
> Following peer dependencies are required to use that authorizer:
> * [cryptography](https://pypi.org/project/cryptography/)
> * [jwt](https://pypi.org/project/jwt/)
> * [requests](https://pypi.org/project/requests/)

```py
from python_falcon_authenticator.authenticators.jwt import Authenticator as JwtAuthenticator

authenticator = JwtAuthenticator(
    client_id="CliEnTiD",
    oauth_domain="https://oauth.auth.com",
)
```

| parameter | default value | description |
| --- | --- | --- |
| `client_id` | | **REQUIRED** the expected OAuth Client identifier as defined in the `aud` (audience) field of the [OpenID JWT](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3)
| `oauth_domain` | | **REQUIRED** the identity provider OAuth domain as defined in the `iss` (issuer) field of the [OpenID JWT](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.1) 
| `oidc_uri` | `{oauth_domain}/.well-known/openid-configuration` | URI of the OpenID Connect metadata related to the authentication server as defined in [openid.net](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata). Only the `jwks_uri` attribute is being used
| `context_builder` | `default_context_builder` from `python_falcon_authenticator.authenticators.jwt` | a function to populate a [context](https://falcon.readthedocs.io/en/stable/api/request_and_response_wsgi.html#falcon.Request.context) giving a JWT decoded payload dictionary.

#### Static Basic
Statically provide username and password to match
```py
from python_falcon_authenticator.authenticators.static_basic import Authenticator as BasicAuthenticator

authenticator = BasicAuthenticator(
    username="raphaeljoie",
    password="Passw0rd"
)
```
