"""Read secrets from files, as commonly written by Vault Agent templates."""

from pathlib import Path
from typing import Union

from polyvault.backend.base import SecretBackend
from polyvault.exceptions import SecretNotFoundError


class FileBackend(SecretBackend):
    """Read one secret per file beneath ``directory``."""

    def __init__(self, directory: Union[str, Path] = "/run/secrets", encoding: str = "utf-8"):
        self.directory = Path(directory)
        self.encoding = encoding

    def get_secret(self, name: str) -> str:
        root = self.directory.resolve()
        path = (root / name).resolve()
        if path != root and root not in path.parents:
            raise ValueError("secret name must resolve inside the configured directory")
        try:
            return path.read_text(encoding=self.encoding).rstrip("\r\n")
        except FileNotFoundError as exc:
            raise SecretNotFoundError(name) from exc

