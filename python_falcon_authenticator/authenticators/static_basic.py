import falcon
import base64

from .base_authenticator import BaseAuthenticator


class Authenticator(BaseAuthenticator):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def authorize(self, req, resp, resource, params) -> bool:
        # Ensure Authorization header
        if 'AUTHORIZATION' not in req.headers:
            raise falcon.HTTPUnauthorized(title="Missing Authorization Header")

        authorization = req.headers['AUTHORIZATION']

        # Ensure Bearer Authorization
        bearer_prefix = 'Basic'
        if not authorization.startswith(bearer_prefix):
            raise falcon.HTTPUnauthorized(f"Authorization must be of type {bearer_prefix}")

        username_password_b64 = authorization[len(bearer_prefix)+1:]
        username_password = base64.b64decode(username_password_b64).decode('utf8')
        try:
            [username, password] = username_password.split(":")
        except ValueError:
            raise falcon.HTTPUnauthorized("Authorization Basic must be encoded login:password")

        if username != self.username or password != self.password:
            raise falcon.HTTPUnauthorized("Wrong username or password")

        return True
