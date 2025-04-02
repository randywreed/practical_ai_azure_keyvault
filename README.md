# Practical AI Azure KeyVault

A Python package for managing Azure OpenAI configuration and authentication using Azure Key Vault.

## Directory Structure

Your project should follow this structure for proper installation:
```
practical_ai_azure_keyvault/
├── practical_ai_azure_keyvault/
│   ├── __init__.py
│   └── azure_keyvault.py
├── setup.py
├── pyproject.toml
└── README.md
```

## Installation

### From Git Repository
```bash
# Make sure to use the correct GitHub URL
pip install git+https://github.com/randyreeder/practical_ai_azure_keyvault.git
```

### For Development
```bash
git clone https://github.com/yourusername/practical_ai_azure_keyvault.git
cd practical_ai_azure_keyvault
pip install -e .
```

## Usage

### Basic Usage
```python
from practical_ai_azure_keyvault import initialize_app, AIConfig

# Initialize with your Key Vault name
initialize_app("YourKeyVaultName")

# Access the configuration
config = AIConfig()
print(f"Endpoint: {config.endpoint}")
```

### Authentication Methods

The package supports three authentication methods in order of preference:

1. **Service Principal Authentication** (for automated processes)
```bash
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_TENANT_ID="your-tenant-id"
```

2. **Direct API Access** (for local development)
```bash
export AI_API_KEY="your-api-key"
export AI_ENDPOINT="your-endpoint"
export AI_VERSION="your-api-version"
```

3. **Device Code Authentication** (interactive login)
- No environment variables needed
- Follow the prompts in the console

### Key Vault Requirements

Your Azure Key Vault should contain these secrets:
- `AzureOpenAIAPIKey`
- `AzureOpenAIEndpoint`
- `AzureOpenAIVersion`

## License

MIT License