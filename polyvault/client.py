"""The unified public interface for retrieving secrets."""

from pathlib import Path
from typing import Optional, Union

from polyvault.backend.base import SecretBackend
from polyvault.backend.file import FileBackend


class PolyVault:
    """Retrieve secrets through a selected backend.

    With no backend supplied, secrets are read from individual files in
    ``/run/secrets`` (the common Vault Agent template destination).
    """

    def __init__(
        self,
        backend: Optional[SecretBackend] = None,
        secret_dir: Union[str, Path] = "/run/secrets",
    ):
        self.backend = backend if backend is not None else FileBackend(secret_dir)

    def get_secret(self, name: str) -> str:
        """Return the named secret as text."""
        return self.backend.get_secret(name)

