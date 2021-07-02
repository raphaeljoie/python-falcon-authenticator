from abc import ABC, abstractmethod


class BaseAuthenticator(ABC):
    @abstractmethod
    def authorize(self, req, resp, resource, params) -> bool:
        pass
