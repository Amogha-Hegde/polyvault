"""PolyVault provides one interface for secrets from multiple backends."""

from polyvault.backend import (
    AWSSecretsManagerBackend,
    AzureKeyVaultBackend,
    EnvBackend,
    FileBackend,
    SecretBackend,
    VaultBackend,
)
from polyvault.client import PolyVault
from polyvault.exceptions import (
    BackendConfigurationError,
    BackendDependencyError,
    PolyVaultError,
    SecretAlreadyExistsError,
    SecretNotFoundError,
    UnsupportedOperationError,
)

__all__ = [
    "PolyVault",
    "SecretBackend",
    "FileBackend",
    "EnvBackend",
    "AWSSecretsManagerBackend",
    "AzureKeyVaultBackend",
    "VaultBackend",
    "PolyVaultError",
    "SecretNotFoundError",
    "SecretAlreadyExistsError",
    "BackendConfigurationError",
    "BackendDependencyError",
    "UnsupportedOperationError",
]
