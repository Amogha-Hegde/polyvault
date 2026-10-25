"""The unified public interface for retrieving secrets."""

from pathlib import Path
from typing import Any, Optional, Union

from polyvault.backend.base import SecretBackend
from polyvault.backend.file import FileBackend
from polyvault.exceptions import SecretNotFoundError


_DEFAULT_NOT_SET = object()


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

    def get_secret(self, name: str, default: Any = _DEFAULT_NOT_SET) -> Any:
        """Return a secret, or ``default`` if it is missing.

        If no default is provided, a missing secret raises
        :class:`SecretNotFoundError`.
        """
        try:
            return self.backend.get_secret(name)
        except SecretNotFoundError:
            if default is _DEFAULT_NOT_SET:
                raise
            return default

