from __future__ import annotations

from typing import TYPE_CHECKING, Union, List

import falcon

from .resource_auth_config import ResourceAuthConfig

if TYPE_CHECKING:
    from .authenticators import BaseAuthenticator


class PythonFalconAuthenticator:
    RESOURCE_AUTH_CONFIG_ATTR = "auth_config"

    def __init__(self, authenticators: Union[BaseAuthenticator, List[BaseAuthenticator]],
                 exempt_routes=None, exempt_methods=None):
        self.authenticators: List[BaseAuthenticator] = authenticators if isinstance(authenticators, list) else [authenticators]

    def process_resource(self, req, resp, resource, params):
        if hasattr(resource, PythonFalconAuthenticator.RESOURCE_AUTH_CONFIG_ATTR):
            resource_auth_config = getattr(resource, self.RESOURCE_AUTH_CONFIG_ATTR)
            assert isinstance(resource_auth_config, ResourceAuthConfig), \
                f"Expected {type(ResourceAuthConfig)} for authorization config of {resource} but " \
                f"found {type(resource_auth_config)} type at attr {PythonFalconAuthenticator.RESOURCE_AUTH_CONFIG_ATTR}"

            if resource_auth_config.should_skip(req, params):
                return

        errors = []
        for authenticator in self.authenticators:
            try:
                if authenticator.authenticate(req, resp, resource, params):
                    return
            except falcon.HTTPUnauthorized as e:
                errors.append(e)
            except falcon.HTTPForbidden as e:
                errors.append(e)

        if len(errors):
            raise errors[0]
