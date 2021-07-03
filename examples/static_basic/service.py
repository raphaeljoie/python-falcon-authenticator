import falcon
from python_falcon_authenticator import PythonFalconAuthorizer
from python_falcon_authenticator.authenticators.static_basic import Authenticator as BasicAuthenticator


# Auth0 client ID
client_id = "CLIENT_ID"
# Auth0 domain
oauth_api = "https://XXX.eu.auth0.com/"

authenticator = PythonFalconAuthorizer(
    BasicAuthenticator(
        username="raphaeljoie",
        password="Passw0rd",
    )
)


class UsersResource:
    def on_get(self, req, resp):
        resp.media = [{"id": "raphaeljoie"}]


api = falcon.API(middleware=[authenticator])

api.add_route("/users", UsersResource())
