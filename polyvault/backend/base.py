"""Base interface for secret backends."""

from abc import ABC, abstractmethod

from polyvault.exceptions import UnsupportedOperationError


class SecretBackend(ABC):
    """A source that supports CRUD operations for secrets."""

    @abstractmethod
    def get_secret(self, name: str) -> str:
        """Return a secret as text, or raise an appropriate PolyVault error."""

    def create_secret(self, name: str, value: str) -> None:
        """Create a secret, failing if it already exists."""
        raise UnsupportedOperationError("create_secret is not supported by this backend")

    def update_secret(self, name: str, value: str) -> None:
        """Replace the value of an existing secret."""
        raise UnsupportedOperationError("update_secret is not supported by this backend")

    def delete_secret(self, name: str) -> None:
        """Delete a secret, or raise SecretNotFoundError if it is absent."""
        raise UnsupportedOperationError("delete_secret is not supported by this backend")

