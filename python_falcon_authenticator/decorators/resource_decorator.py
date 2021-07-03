from .. import ResourceAuthConfig
from .. import PythonFalconAuthenticator


def resource_auth_config(*args, **kwargs):
    def decorator(original_class):
        # TODO what if there is already an auth config?
        setattr(original_class, PythonFalconAuthenticator.RESOURCE_AUTH_CONFIG_ATTR, ResourceAuthConfig(*args, **kwargs))
        return original_class

    return decorator
