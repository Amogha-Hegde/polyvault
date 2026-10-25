"""Read secrets from environment variables."""

import os

from polyvault.backend.base import SecretBackend
from polyvault.exceptions import SecretNotFoundError


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

