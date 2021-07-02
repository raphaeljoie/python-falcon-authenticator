from .jwt import Authenticator as JwtAuthenticator


class Authenticator(JwtAuthenticator):
    DEFAULT_OAUTH_API_TEMPLATE = "https://login.microsoftonline.com/${TENANT_ID}/v2.0"

    def __init__(self, tenant_id, **kwargs):
        oauth_api = self.DEFAULT_OAUTH_API_TEMPLATE.replace('${TENANT_ID}', str(tenant_id))

        super().__init__(oauth_api=oauth_api, **kwargs)
