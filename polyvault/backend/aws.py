"""AWS Secrets Manager backend."""

from typing import Optional

from polyvault.backend.base import SecretBackend
from polyvault.exceptions import (
    BackendDependencyError,
    SecretAlreadyExistsError,
    SecretNotFoundError,
)


class AWSSecretsManagerBackend(SecretBackend):
    """Retrieve secrets by AWS Secrets Manager secret ID."""

    def __init__(self, region_name: Optional[str] = None, client=None):
        if client is None:
            try:
                import boto3
            except ImportError as exc:
                raise BackendDependencyError(
                    "AWS backend requires the optional dependency: pip install 'polyvault[aws]'"
                ) from exc
            client = boto3.client("secretsmanager", region_name=region_name)
        self.client = client

    def get_secret(self, name: str) -> str:
        try:
            response = self.client.get_secret_value(SecretId=name)
        except Exception as exc:
            if getattr(exc, "response", {}).get("Error", {}).get("Code") in {
                "ResourceNotFoundException", "NotFoundException"
            }:
                raise SecretNotFoundError(name) from exc
            raise
        if "SecretString" in response:
            return response["SecretString"]
        return response["SecretBinary"].decode("utf-8")

    def create_secret(self, name: str, value: str) -> None:
        try:
            self.client.create_secret(Name=name, SecretString=value)
        except Exception as exc:
            if self._error_code(exc) == "ResourceExistsException":
                raise SecretAlreadyExistsError(name) from exc
            raise

    def update_secret(self, name: str, value: str) -> None:
        try:
            self.client.put_secret_value(SecretId=name, SecretString=value)
        except Exception as exc:
            if self._error_code(exc) == "ResourceNotFoundException":
                raise SecretNotFoundError(name) from exc
            raise

    def delete_secret(self, name: str) -> None:
        try:
            self.client.delete_secret(SecretId=name)
        except Exception as exc:
            if self._error_code(exc) in {"ResourceNotFoundException", "NotFoundException"}:
                raise SecretNotFoundError(name) from exc
            raise

    @staticmethod
    def _error_code(exc: Exception):
        return getattr(exc, "response", {}).get("Error", {}).get("Code")

