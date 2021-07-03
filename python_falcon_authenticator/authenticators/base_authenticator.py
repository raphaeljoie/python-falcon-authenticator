from abc import ABC, abstractmethod


class BaseAuthenticator(ABC):
    @abstractmethod
    def authenticate(self, req, resp, resource, params) -> bool:
        pass
