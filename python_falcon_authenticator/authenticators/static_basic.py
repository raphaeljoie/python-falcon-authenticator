import falcon
import base64

from .base_authenticator import BaseAuthenticator
from .error_codes import MISSING_AUTHORIZATION_HEADER, UNEXPECTED_AUTHORIZATION_HEADER_TYPE, WRONG_CREDENTIALS, \
    BAD_AUTHORIZATION_HEADER_CREDENTIALS


class Authenticator(BaseAuthenticator):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    def authenticate(self, req, resp, resource, params) -> bool:
        # Ensure Authorization header
        if 'AUTHORIZATION' not in req.headers:
            raise falcon.HTTPUnauthorized(title="Missing Authorization Header",
                                          code=MISSING_AUTHORIZATION_HEADER)

        authorization = req.headers['AUTHORIZATION']

        # Ensure Bearer Authorization
        bearer_prefix = 'Basic '
        if not authorization.startswith(bearer_prefix):
            raise falcon.HTTPUnauthorized(title=f"Authorization must be of type {bearer_prefix[:-1]}",
                                          code=UNEXPECTED_AUTHORIZATION_HEADER_TYPE)

        try:
            username_password_b64 = authorization[len(bearer_prefix):]
            username_password = base64.b64decode(username_password_b64).decode('utf8')
            [username, password] = username_password.split(":")
        except ValueError:
            raise falcon.HTTPUnauthorized(title="Authorization Basic must be base64 encoded <login>:<password> string",
                                          code=BAD_AUTHORIZATION_HEADER_CREDENTIALS)

        if username != self.username or password != self.password:
            raise falcon.HTTPUnauthorized(title="Wrong username or password",
                                          code=WRONG_CREDENTIALS)

        return True
