import base64
import json
import urllib.parse

import falcon
import jwt
import requests

from .base_authenticator import BaseAuthenticator
from ..utils_cryptography import jwk_to_public_key


def default_context_builder(context, jwt_body):
    context.user_id = jwt_body.get('sub')


class JwkServerException(Exception):
    pass


# noinspection PyBroadException
def safe_get_jwt_body_attr(body64, attr):
    try:
        return json.loads(base64.b64decode(body64)).get(attr)
    except:
        return None


class Authenticator(BaseAuthenticator):
    def __init__(self, client_id, oauth_api, context_builder=None, oidc_uri: str = None):
        assert isinstance(client_id, str)

        self.client_id = client_id
        self.oauth_api = oauth_api
        self.context_builder = context_builder or default_context_builder
        self.oidc_uri = oidc_uri or urllib.parse.urljoin(self.oauth_api, '.well-known/openid-configuration')

        self.jwks_uri = None  # could try self.oauth_api + .well-known/jwks.json
        self.jwks = {}
        self.public_keys = {}

    def authenticate(self, req, resp, resource, params) -> bool:
        # Ensure Authorization header
        if 'AUTHORIZATION' not in req.headers:
            raise falcon.HTTPUnauthorized(title="Missing Authorization Header")

        authorization = req.headers['AUTHORIZATION']

        # Ensure Bearer Authorization
        bearer_prefix = 'Bearer '
        # https://forums.aws.amazon.com/message.jspa?messageID=773958
        if not authorization.startswith(bearer_prefix):
            raise falcon.HTTPUnauthorized("Authorization must be of type Bearer")

        # Ensure JWT formatting
        token = authorization[len(bearer_prefix):]
        try:
            [header64, body64, signature] = token.split(".")
        except ValueError:
            raise falcon.HTTPUnauthorized("Authorization Bearer must be a three part JWT token")

        # Decode base 64 encoded JWT header
        try:
            header = json.loads(base64.b64decode(header64))
        except json.JSONDecodeError:
            raise falcon.HTTPUnauthorized("Unable to parse JWT header. It must be a base64 encoded JSON dictionary")

        # Ensure key id is in JWT header
        if 'kid' not in header:
            raise falcon.HTTPUnauthorized("Missing 'kid' in JWT header")

        public_key = self.get_public_key(header['kid'])

        issuer = self.oauth_api
        audience = self.client_id

        try:
            decoded = jwt.decode(token, public_key, audience=audience, issuer=issuer, algorithms='RS256')
        except jwt.exceptions.ExpiredSignatureError:
            raise falcon.HTTPUnauthorized("Token expired (exp)")
        except jwt.exceptions.InvalidSignatureError:
            raise falcon.HTTPUnauthorized("Bad token signature")
        except jwt.exceptions.InvalidAudienceError:
            raise falcon.HTTPUnauthorized(f"Token audience (aud) must be {audience} "
                                          f"but found '{safe_get_jwt_body_attr(body64, 'aud')}' instead")
        except jwt.exceptions.InvalidIssuerError:
            raise falcon.HTTPUnauthorized(f"Token issuer (iss) must be '{issuer}' "
                                          f"but found '{safe_get_jwt_body_attr(body64, 'iss')}' instead")

        self.context_builder(req.context, decoded)
        return True

    def get_public_key(self, kid):
        if kid not in self.public_keys:
            jwk = self.get_jwk(kid)

            if jwk is None:
                # TODO maybe it happens because the token is outdated => check first that date
                raise falcon.HTTPUnauthorized(f"Could not find JWK with id '{kid}' within available JWKs")

            self.public_keys[kid] = jwk_to_public_key(jwk)

        return self.public_keys[kid]

    def get_jwk(self, kid):
        if kid not in self.jwks:
            self.refresh_jwks()

        return self.jwks.get(kid, None)

    def refresh_jwks(self):
        jwks_uri = self.get_jwks_uri()
        resp = requests.get(jwks_uri)

        if not resp.ok:
            raise falcon.HTTPInternalServerError(
                "Failed to load JWKS",
                description=f"Couldn't load JWKS from {jwks_uri}. Got {resp.status_code} response: {resp.text}"
            )

        # TODO also print nice error when not JSON
        resp = resp.json()
        self.jwks = {}
        for _ in resp.get('keys', []):
            self.jwks[_['kid']] = _

    def get_jwks_uri(self):
        if self.jwks_uri is None:
            # TODO what if request fails (not only response NOK but connectivity error)
            resp = requests.get(self.oidc_uri)

            if not resp.ok:
                raise falcon.HTTPInternalServerError(
                    f"Failed to discover JWK uri loading OIDC (OpenID Configuration)",
                    description=f"Tried to load from {self.oidc_uri} bot got response {resp.status_code}: {str(resp.text)}")

            # TODO what if not JSON? => cover that case too
            resp = resp.json()
            if 'jwks_uri' not in resp:
                raise falcon.HTTPInternalServerError(
                    f"Attribute 'jwks_uri' not found in OIDC (OpenID Configuration)",
                    description=f"Successfully loaded OIDC configuration, but not able to foind jwks uri attribute"
                                f" within the response returned: {resp}")

            self.jwks_uri = resp['jwks_uri']

        return self.jwks_uri
