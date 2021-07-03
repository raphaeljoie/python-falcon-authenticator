from .jwt import Authenticator as JwtAuthenticator


class Authenticator(JwtAuthenticator):
    DEFAULT_OAUTH_DOMAIN_TEMPLATE = "https://login.microsoftonline.com/${TENANT_ID}/v2.0"

    def __init__(self, tenant_id, **kwargs):
        oauth_domain = self.DEFAULT_OAUTH_DOMAIN_TEMPLATE.replace('${TENANT_ID}', str(tenant_id))

        super().__init__(oauth_domain=oauth_domain, **kwargs)
