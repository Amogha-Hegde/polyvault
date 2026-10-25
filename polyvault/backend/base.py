"""Base interface for secret backends."""

from abc import ABC, abstractmethod


class SecretBackend(ABC):
    """A source that can retrieve a secret by name."""

    @abstractmethod
    def get_secret(self, name: str) -> str:
        """Return a secret as text, or raise an appropriate PolyVault error."""

