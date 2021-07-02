from typing import Optional, List


class ResourceAuthConfig:
    def __init__(self, skip_methods: Optional[List[str]], skip_uris=Optional[List[str]],
                 skip_responders=Optional[List[str]]):
        self.skip_methods = skip_methods or []
        self.skip_uris = skip_uris or []
        self.skip_responders = skip_responders or []

    def should_skip(self, req, params: Optional[dict] = None) -> bool:
        if req.uri_template in self.skip_uris:
            return True
        if req.method.upper() in self.skip_methods:
            return True

        if len(self.skip_responders) and not hasattr(req, 'responder'):
            raise Exception(f"for using 'skip_responders' option, Falcon must be configured with a 'router' that fills"
                            " the 'responder' attribute of the 'req' object.")

        if hasattr(req, 'responder') and req.responder in self.skip_responders:
            return True

        return False
