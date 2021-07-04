import base64
import unittest
import uuid

import falcon

from python_falcon_authenticator.authenticators.error_codes import MISSING_AUTHORIZATION_HEADER, \
    UNEXPECTED_AUTHORIZATION_HEADER_TYPE, EMPTY_AUTHORIZATION_HEADER_CREDENTIALS, WRONG_CREDENTIALS, \
    BAD_AUTHORIZATION_HEADER_CREDENTIALS
from python_falcon_authenticator.authenticators.static_basic import Authenticator


class Request:
    def __init__(self, headers):
        self.headers = headers


class TestStaticBasicAuthenticator(unittest.TestCase):

    def test_success(self):
        username = str(uuid.uuid4())
        password = str(uuid.uuid4())
        authenticator = Authenticator(username=username, password=password)

        header = base64.b64encode(f"{username}:{password}".encode("utf8")).decode('ascii')

        self.assertTrue(authenticator.authenticate(Request({
                    'AUTHORIZATION': f'Basic {header}'
                }), None, None, None))

    def test_missing_authorization_header(self):
        with self.assertRaises(falcon.HTTPUnauthorized) as exception:
            authenticator = Authenticator(username="", password="")

            self.assertTrue(authenticator.authenticate(Request({}), None, None, None))

        self.assertEqual(MISSING_AUTHORIZATION_HEADER, exception.exception.code)

    def test_unexpected_authorization_header_type(self):
        with self.assertRaises(falcon.HTTPUnauthorized) as exception:
            authenticator = Authenticator(username="", password="")

            self.assertTrue(authenticator.authenticate(Request({'AUTHORIZATION': 'Blabetiblou'}), None, None, None))

        self.assertEqual(UNEXPECTED_AUTHORIZATION_HEADER_TYPE, exception.exception.code)

    def test_empty_authorization_header_credentials(self):
        with self.assertRaises(falcon.HTTPUnauthorized) as exception:
            authenticator = Authenticator(username="", password="")

            self.assertTrue(authenticator.authenticate(Request({'AUTHORIZATION': 'Basic '}), None, None, None))

        self.assertEqual(EMPTY_AUTHORIZATION_HEADER_CREDENTIALS, exception.exception.code)

    def test_non_base64_header_credentials(self):
        with self.assertRaises(falcon.HTTPUnauthorized) as exception:
            authenticator = Authenticator(username="username", password="Passw0rd")

            self.assertTrue(authenticator.authenticate(Request({'AUTHORIZATION': f'Basic ç'}), None, None, None))

        self.assertEqual(BAD_AUTHORIZATION_HEADER_CREDENTIALS, exception.exception.code)

    def test_non_padded_base64_header_credentials(self):
        with self.assertRaises(falcon.HTTPUnauthorized) as exception:
            authenticator = Authenticator(username="username", password="Passw0rd")

            self.assertTrue(authenticator.authenticate(Request({'AUTHORIZATION': f'Basic a'}), None, None, None))

        self.assertEqual(BAD_AUTHORIZATION_HEADER_CREDENTIALS, exception.exception.code)

    def test_missing_column(self):
        with self.assertRaises(falcon.HTTPUnauthorized) as exception:
            authenticator = Authenticator(username="username", password="Passw0rd")

            header = base64.b64encode(f"usernamepassword".encode("utf8")).decode('ascii')
            self.assertTrue(authenticator.authenticate(Request({'AUTHORIZATION': f'Basic {header}'}), None, None, None))

        self.assertEqual(BAD_AUTHORIZATION_HEADER_CREDENTIALS, exception.exception.code)

    def test_extra_column(self):
        with self.assertRaises(falcon.HTTPUnauthorized) as exception:
            authenticator = Authenticator(username="username", password="Passw0rd")

            header = base64.b64encode(f"username:password:password".encode("utf8")).decode('ascii')
            self.assertTrue(authenticator.authenticate(Request({'AUTHORIZATION': f'Basic {header}'}), None, None, None))

        self.assertEqual(BAD_AUTHORIZATION_HEADER_CREDENTIALS, exception.exception.code)

    def test_wrong_credentials(self):
        with self.assertRaises(falcon.HTTPUnauthorized) as exception:
            authenticator = Authenticator(username="username", password="Passw0rd")

            header = base64.b64encode(f"username:password".encode("utf8")).decode('ascii')
            self.assertTrue(authenticator.authenticate(Request({'AUTHORIZATION': f'Basic {header}'}), None, None, None))

        self.assertEqual(WRONG_CREDENTIALS, exception.exception.code)
