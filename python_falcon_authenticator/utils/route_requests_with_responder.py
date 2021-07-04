import falcon


def find_with_request_responder(original_find, router, uri, req=None):
    """
    Execute an original `find` function on a given router using provided argument according to Falcon doc,
    populate req.responder with the responder name (if any), and finally return the value returned by the original
    `find` function
    """
    out = original_find(router, uri, req)

    if req and out:
        responder = out[1].get(req.method)
        if responder:
            req.responder = responder.__name__
    return out


class RouterWithRequestResponder(falcon.routing.DefaultRouter):
    """
    api = falcon.App(router=RouterWithRequestResponder())
    """
    def find(self, uri, req=None):
        return find_with_request_responder(super().find.__func__, self, uri, req)


def with_request_responder(router):
    """
    wrap the `find` method of a router around a new function that is calling the original function
    then filling the req.responder property properly

    api = falcon.App(router=with_request_responder(original_router))
    api = falcon.App(router=with_request_responder(falcon.routing.DefaultRouter()))
    """
    # get Class from which the router was created
    router_class = router if isinstance(router, type) else router.__class__
    # extract the original "find" method to be wrapped
    find_original = getattr(router_class, 'find')

    # define the new `find` method
    def find(self, uri, req=None):
        return find_with_request_responder(find_original.__call__, self, uri, req)

    # replace the method with the new version
    router_class.find = find

    # and return the modified router
    return router
