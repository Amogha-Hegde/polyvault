# PolyVault

PolyVault provides a common CRUD interface for secrets stored in files,
environment variables, AWS Secrets Manager, Azure Key Vault, HashiCorp Vault,
and OpenBao.

## Scope

The shared interface supports four secret operations: create, read, update, and
delete. The file and environment backends implement only these CRUD operations;
they do not provide listing or Vault administration features. Environment
changes affect only the current Python process.

PolyVault does not wrap provider-specific features such as Vault auth methods,
policies, leases, mounts, or audit devices. For Vault/OpenBao, the underlying
`hvac` client is available as `secrets.backend.client` when those features are
needed. Operation details such as deletion recovery and version history follow
the selected provider's behavior.

## Default: files

With no backend configured, PolyVault reads one secret per file from
`/run/secrets`, a common destination for Vault Agent templates:

```python
from polyvault import PolyVault

secrets = PolyVault()
database_password = secrets.get_secret("database-password")
optional_value = secrets.get_secret("optional-setting", default="fallback")
```

If no default is provided, a missing secret raises `SecretNotFoundError`. To
use another directory, pass it as `secret_dir`:

```python
secrets = PolyVault(secret_dir="./secrets")
```

File-backed CRUD methods operate on files under that directory. For files
managed by Vault Agent, agent rendering may replace local changes.

## Environment variables

Pass a backend instance to select a different source:

```python
from polyvault import EnvBackend, PolyVault

secrets = PolyVault(backend=EnvBackend(prefix="APP_"))
api_key = secrets.get_secret("API_KEY")  # reads APP_API_KEY
```

## Provider backends

Install the optional extra for the provider you use:

```shell
pip install 'polyvault[aws]'
pip install 'polyvault[azure]'
pip install 'polyvault[hashicorp]'  # also supports OpenBao
```

Then pass `AWSSecretsManagerBackend`, `AzureKeyVaultBackend`, or
`VaultBackend` from `polyvault.backend` to `PolyVault`. Configure Azure with its
Key Vault URL. Configure Vault/OpenBao with its API URL, KV mount point, and KV
version. Provider clients are loaded only when their backend is initialized.
