"""Azure Key Vault backend."""

from polyvault.backend.base import SecretBackend
from polyvault.exceptions import BackendConfigurationError, BackendDependencyError, SecretNotFoundError


class AzureKeyVaultBackend(SecretBackend):
    """Retrieve secrets from Azure Key Vault by secret name."""

    def __init__(self, vault_url: str, credential=None, client=None):
        if client is None:
            if not vault_url:
                raise BackendConfigurationError("vault_url is required for Azure Key Vault")
            try:
                from azure.identity import DefaultAzureCredential
                from azure.keyvault.secrets import SecretClient
            except ImportError as exc:
                raise BackendDependencyError(
                    "Azure backend requires: pip install 'polyvault[azure]'"
                ) from exc
            credential = credential or DefaultAzureCredential()
            client = SecretClient(vault_url=vault_url, credential=credential)
        self.client = client

    def get_secret(self, name: str) -> str:
        try:
            return self.client.get_secret(name).value
        except Exception as exc:
            if exc.__class__.__name__ in {"ResourceNotFoundError", "KeyVaultSecretNotFoundError"}:
                raise SecretNotFoundError(name) from exc
            raise

