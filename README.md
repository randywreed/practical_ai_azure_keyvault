# Practical AI Azure KeyVault

A Python package for managing Azure OpenAI configuration and authentication using Azure Key Vault.

## Installation

You can install this package directly from GitHub:

```bash
pip install git+https://github.com/yourusername/practical_ai_azure_keyvault.git
```

Replace `yourusername` with your GitHub username.

## Usage

### Initialization

To use the package, you need to initialize the configuration by specifying the Key Vault name. The package supports multiple authentication methods:

1. **Service Principal Authentication** (Recommended for automated server-to-server authentication)
2. **Environment Variables** (For local development)
3. **Device Code Authentication** (Interactive login for development)

Here is an example of how to initialize the configuration:

```python
from practical_ai_azure_keyvault import initialize_app

# Specify the Key Vault name
initialize_app("YourKeyVaultName")
```

### Environment Variables

Set the following environment variables based on your preferred authentication method:

#### Service Principal Authentication
```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
```

#### Direct API Access
```bash
export AI_API_KEY="your-api-key"
export AI_ENDPOINT="your-endpoint"
export AI_VERSION="your-api-version"
```

### Key Vault Secrets

If using Azure Key Vault, ensure the following secrets are stored in your Key Vault:

- `AzureOpenAIAPIKey`
- `AzureOpenAIEndpoint`
- `AzureOpenAIVersion`

### Example

```python
from practical_ai_azure_keyvault import AIConfig, initialize_app

# Initialize the configuration with your Key Vault name
initialize_app("YourKeyVaultName")

# Access the global AIConfig instance
ai_config = AIConfig()

# Use the configuration
print(f"API Key: {ai_config.api_key}")
print(f"Endpoint: {ai_config.endpoint}")
print(f"API Version: {ai_config.api_version}")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.