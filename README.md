# PolyVault

PolyVault provides one interface for retrieving secrets from files, environment
variables, AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, and OpenBao.

## Default: files

The default backend reads one secret per file from `/run/secrets`, a common
destination for files rendered by Vault Agent templates:

```python
from polyvault import PolyVault

secrets = PolyVault()
database_password = secrets.get_secret("database-password")
# Missing secrets raise SecretNotFoundError unless a default is supplied.
optional_value = secrets.get_secret("optional-setting", default="fallback")

secrets.create_secret("new-secret", "first value")
secrets.update_secret("new-secret", "replacement value")
secrets.delete_secret("new-secret")
```

The file and environment backends support CRUD. Environment changes apply only
to the current Python process. Vault/OpenBao's underlying `hvac` client is
available as `secrets.backend.client` for Vault-specific APIs beyond CRUD.

Set a different directory with `PolyVault(secret_dir="./secrets")`.

## Other backends

Pass a backend instance to `PolyVault` to select another source:

```python
from polyvault import EnvBackend, PolyVault

secrets = PolyVault(backend=EnvBackend(prefix="APP_"))
api_key = secrets.get_secret("API_KEY")  # reads APP_API_KEY
```

Provider SDKs are optional. Install only the extra you use:

```shell
pip install 'polyvault[aws]'
pip install 'polyvault[azure]'
pip install 'polyvault[hashicorp]'  # also supports OpenBao
```

Then pass `AWSSecretsManagerBackend`, `AzureKeyVaultBackend`, or `VaultBackend`
from `polyvault.backend` to `PolyVault`. The Vault backend accepts the Vault
API URL, KV mount point, and KV version; it can connect to HashiCorp Vault or
OpenBao.
