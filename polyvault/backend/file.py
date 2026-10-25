"""Read secrets from files, as commonly written by Vault Agent templates."""

from pathlib import Path
from typing import Union

from polyvault.backend.base import SecretBackend
from polyvault.exceptions import SecretAlreadyExistsError, SecretNotFoundError


class FileBackend(SecretBackend):
    """Read one secret per file beneath ``directory``."""

    def __init__(self, directory: Union[str, Path] = "/run/secrets", encoding: str = "utf-8"):
        self.directory = Path(directory)
        self.encoding = encoding

    def get_secret(self, name: str) -> str:
        path = self._path_for(name)
        try:
            return path.read_text(encoding=self.encoding).rstrip("\r\n")
        except FileNotFoundError as exc:
            raise SecretNotFoundError(name) from exc

    def create_secret(self, name: str, value: str) -> None:
        path = self._path_for(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with path.open("x", encoding=self.encoding) as secret_file:
                secret_file.write(value)
        except FileExistsError as exc:
            raise SecretAlreadyExistsError(name) from exc

    def update_secret(self, name: str, value: str) -> None:
        path = self._path_for(name)
        if not path.is_file():
            raise SecretNotFoundError(name)
        path.write_text(value, encoding=self.encoding)

    def delete_secret(self, name: str) -> None:
        path = self._path_for(name)
        try:
            path.unlink()
        except FileNotFoundError as exc:
            raise SecretNotFoundError(name) from exc

    def _path_for(self, name: str) -> Path:
        root = self.directory.resolve()
        path = (root / name).resolve()
        if path != root and root not in path.parents:
            raise ValueError("secret name must resolve inside the configured directory")
        return path

