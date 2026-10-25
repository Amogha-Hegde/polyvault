"""Exceptions shared by PolyVault backends."""


class PolyVaultError(Exception):
    """Base class for PolyVault errors."""


class SecretNotFoundError(PolyVaultError, KeyError):
    """Raised when a backend cannot find the requested secret."""


class SecretAlreadyExistsError(PolyVaultError):
    """Raised when creating a secret whose name is already in use."""


class BackendConfigurationError(PolyVaultError, ValueError):
    """Raised when a backend is missing required configuration."""


class BackendDependencyError(PolyVaultError, ImportError):
    """Raised when an optional provider SDK is not installed."""


class UnsupportedOperationError(PolyVaultError, NotImplementedError):
    """Raised when a backend does not support a requested operation."""
