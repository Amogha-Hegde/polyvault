"""Read secrets from environment variables."""

import os

from polyvault.backend.base import SecretBackend
from polyvault.exceptions import SecretAlreadyExistsError, SecretNotFoundError


class EnvBackend(SecretBackend):
    """Read a secret from an environment variable, optionally with a prefix."""

    def __init__(self, prefix: str = ""):
        self.prefix = prefix

    def get_secret(self, name: str) -> str:
        key = f"{self.prefix}{name}"
        try:
            return os.environ[key]
        except KeyError as exc:
            raise SecretNotFoundError(key) from exc

    def create_secret(self, name: str, value: str) -> None:
        key = f"{self.prefix}{name}"
        if key in os.environ:
            raise SecretAlreadyExistsError(key)
        os.environ[key] = value

    def update_secret(self, name: str, value: str) -> None:
        key = f"{self.prefix}{name}"
        if key not in os.environ:
            raise SecretNotFoundError(key)
        os.environ[key] = value

    def delete_secret(self, name: str) -> None:
        key = f"{self.prefix}{name}"
        try:
            del os.environ[key]
        except KeyError as exc:
            raise SecretNotFoundError(key) from exc

