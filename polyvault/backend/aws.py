"""AWS Secrets Manager backend."""

from typing import Optional

from polyvault.backend.base import SecretBackend
from polyvault.exceptions import BackendDependencyError, SecretNotFoundError


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

