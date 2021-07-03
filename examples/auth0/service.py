import falcon
from python_falcon_authenticator import PythonFalconAuthenticator
from python_falcon_authenticator.authenticators.jwt import Authenticator as JwtAuthenticator
from python_falcon_authenticator.decorators import resource_auth_config
from python_falcon_authenticator.utils.route_requests_with_responder import RouterWithRequestResponder


# Auth0 client ID
client_id = "CLIENT_ID"
# Auth0 domain
oauth_domain = "https://XXX.eu.auth0.com/"

authenticator = PythonFalconAuthenticator(
    JwtAuthenticator(
        client_id=client_id,
        oauth_domain=oauth_domain,
    )
)


@resource_auth_config(
    skip_methods=['POST'],  # skip a given method
    skip_uris=['/users'],  # skip a given uri TEMPLATE used in add_route())
    skip_responders=['on_post', 'on_get_skipped']  # skip a responder name
)
class UsersResource:
    def on_post(self, req, resp):
        # The authorization of this endpoint is skipped because of the
        # three skip conditions
        resp.media = {"hello": "world"}

    def on_get(self, req, resp):
        # This one is skipped only because of skip_uris
        resp.media = {"hello": "world"}

    def on_get_not_skipped(self, req, resp):
        # not skipped
        resp.media = {"hello": "world"}

    def on_get_skipped(self, req, resp):
        # not skipped
        resp.media = {"hello": "world"}


api = falcon.API(middleware=[authenticator], router=RouterWithRequestResponder())

api.add_route("/users", UsersResource())
api.add_route("/users/not_skipped", UsersResource(), suffix="not_skipped")
api.add_route("/users/skipped", UsersResource(), suffix="skipped")
