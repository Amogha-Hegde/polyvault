"""HashiCorp Vault and OpenBao backend using the Vault-compatible API."""

from typing import Optional

from polyvault.backend.base import SecretBackend
from polyvault.exceptions import (
    BackendConfigurationError,
    BackendDependencyError,
    SecretAlreadyExistsError,
    SecretNotFoundError,
)


class VaultBackend(SecretBackend):
    """Read KV secrets from HashiCorp Vault or OpenBao using ``hvac``."""

    def __init__(
        self,
        url: str,
        token: Optional[str] = None,
        mount_point: str = "secret",
        kv_version: int = 2,
        client=None,
    ):
        if client is None:
            if not url:
                raise BackendConfigurationError("url is required for Vault/OpenBao")
            try:
                import hvac
            except ImportError as exc:
                raise BackendDependencyError(
                    "Vault/OpenBao backend requires: pip install 'polyvault[hashicorp]'"
                ) from exc
            client = hvac.Client(url=url, token=token)
        if kv_version not in (1, 2):
            raise BackendConfigurationError("kv_version must be 1 or 2")
        self.client = client
        self.mount_point = mount_point
        self.kv_version = kv_version

    def get_secret(self, name: str) -> str:
        try:
            if self.kv_version == 2:
                response = self.client.secrets.kv.v2.read_secret_version(
                    path=name, mount_point=self.mount_point
                )
                data = response["data"]["data"]
            else:
                response = self.client.secrets.kv.v1.read_secret(
                    path=name, mount_point=self.mount_point
                )
                data = response["data"]
        except Exception as exc:
            if exc.__class__.__name__ in {"InvalidPath", "SecretNotFound"}:
                raise SecretNotFoundError(name) from exc
            raise
        if "value" in data and len(data) == 1:
            return str(data["value"])
        import json

        return json.dumps(data)

    def create_secret(self, name: str, value: str) -> None:
        data = self._as_data(value)
        try:
            if self.kv_version == 2:
                self.client.secrets.kv.v2.create_or_update_secret(
                    path=name, secret=data, mount_point=self.mount_point, cas=0
                )
            else:
                self._ensure_missing(name)
                self.client.secrets.kv.v1.create_or_update_secret(
                    path=name, secret=data, mount_point=self.mount_point
                )
        except Exception as exc:
            if exc.__class__.__name__ in {"InvalidRequest", "InvalidPath"}:
                raise SecretAlreadyExistsError(name) from exc
            raise

    def update_secret(self, name: str, value: str) -> None:
        try:
            if self.kv_version == 2:
                metadata = self.client.secrets.kv.v2.read_secret_metadata(
                    path=name, mount_point=self.mount_point
                )
                version = metadata["data"]["current_version"]
                self.client.secrets.kv.v2.create_or_update_secret(
                    path=name,
                    secret=self._as_data(value),
                    mount_point=self.mount_point,
                    cas=version,
                )
            else:
                self.client.secrets.kv.v1.read_secret(path=name, mount_point=self.mount_point)
                self.client.secrets.kv.v1.create_or_update_secret(
                    path=name, secret=self._as_data(value), mount_point=self.mount_point
                )
        except Exception as exc:
            if exc.__class__.__name__ in {"InvalidPath", "SecretNotFound"}:
                raise SecretNotFoundError(name) from exc
            raise

    def delete_secret(self, name: str) -> None:
        try:
            if self.kv_version == 2:
                self.client.secrets.kv.v2.delete_latest_version_of_secret(
                    path=name, mount_point=self.mount_point
                )
            else:
                self.client.secrets.kv.v1.delete_secret(path=name, mount_point=self.mount_point)
        except Exception as exc:
            if exc.__class__.__name__ in {"InvalidPath", "SecretNotFound"}:
                raise SecretNotFoundError(name) from exc
            raise

    def _ensure_missing(self, name: str) -> None:
        try:
            self.client.secrets.kv.v1.read_secret(path=name, mount_point=self.mount_point)
        except Exception as exc:
            if exc.__class__.__name__ in {"InvalidPath", "SecretNotFound"}:
                return
            raise
        raise SecretAlreadyExistsError(name)

    @staticmethod
    def _as_data(value: str) -> dict:
        import json

        try:
            parsed = json.loads(value)
        except (TypeError, json.JSONDecodeError):
            return {"value": value}
        return parsed if isinstance(parsed, dict) else {"value": value}

