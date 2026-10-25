"""Exceptions shared by PolyVault backends."""


class PolyVaultError(Exception):
    """Base class for PolyVault errors."""


class SecretNotFoundError(PolyVaultError, KeyError):
    """Raised when a backend cannot find the requested secret."""


class BackendConfigurationError(PolyVaultError, ValueError):
    """Raised when a backend is missing required configuration."""


class BackendDependencyError(PolyVaultError, ImportError):
    """Raised when an optional provider SDK is not installed."""
