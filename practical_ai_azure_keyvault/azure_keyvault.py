import os
from azure.identity import DefaultAzureCredential, InteractiveBrowserCredential, ClientSecretCredential, DeviceCodeCredential
from azure.keyvault.secrets import SecretClient
from openai import AzureOpenAI

class AIConfig:
    """
    Singleton class that manages Azure OpenAI configuration and authentication.
    Attempts multiple authentication methods in order:
    1. Service Principal (automated server-to-server auth)
    2. Environment Variables (local development)
    3. Device Code (interactive login for development)
    """
    _instance = None

    def __new__(cls):
        """Ensure only one instance of AIConfig exists"""
        if cls._instance is None:
            cls._instance = super(AIConfig, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def initialize(self, vault_name):
        """
        Initialize Azure OpenAI configuration using various authentication methods.
        
        The authentication flow tries these methods in order:
        1. Service Principal credentials from environment
        2. Direct API credentials from environment
        3. Interactive device code authentication
        
        Args:
            vault_name (str): The name of your Azure Key Vault instance
            
        Returns:
            bool: True if initialization successful, False otherwise
        """
        if self.initialized:
            return True

        print("Loading configuration...")
        
        # First, try to use environment variables for Key Vault authentication
        try:
            # Check if environment variables for service principal are available
            if all(key in os.environ for key in ["AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID"]):
                print("Using service principal authentication...")
                credential = ClientSecretCredential(
                    client_id=os.environ["AZURE_CLIENT_ID"],
                    client_secret=os.environ["AZURE_CLIENT_SECRET"],
                    tenant_id=os.environ["AZURE_TENANT_ID"]
                )
                
                client = SecretClient(
                    vault_url=f"https://{vault_name}.vault.azure.net",
                    credential=credential
                )
                
                self.api_key = client.get_secret("AzureOpenAIAPIKey").value
                self.endpoint = client.get_secret("AzureOpenAIEndpoint").value
                self.api_version = client.get_secret("AzureOpenAIVersion").value
                
                self.initialized = True
                print("✅ Successfully loaded configuration from Key Vault using service principal!")
                return True
        except Exception as e:
            print(f"Service principal authentication failed: {str(e)}")
        
        # Check if running in Codespace
        in_codespace = os.environ.get('CODESPACES') == 'true'
        
        # Try to load directly from environment variables for the API
        try:
            if all(key in os.environ for key in ["AI_API_KEY", "AI_ENDPOINT", "AI_VERSION"]):
                self.api_key = os.environ["AI_API_KEY"]
                self.endpoint = os.environ["AI_ENDPOINT"]
                self.api_version = os.environ["AI_VERSION"]

                self.initialized = True
                print("✅ Successfully loaded configuration from environment!")
                return True
        except Exception as e:
            print(f"Environment variable loading failed: {str(e)}")
            
        # If still not initialized, try Key Vault with interactive auth
        try:
            print("Trying Key Vault with device code authentication...")
            
            # Use device code credential which doesn't rely on browser redirects
            credential = DeviceCodeCredential(
                additionally_allowed_tenants=["*"],  # Allow any tenant
                user_prompt=lambda message: print(f"\n{message}\n")
            )
            
            print("Please follow the instructions to authenticate:")
            
            client = SecretClient(
                vault_url=f"https://{vault_name}.vault.azure.net",
                credential=credential
            )

            self.api_key = client.get_secret("AzureOpenAIAPIKey").value
            self.endpoint = client.get_secret("AzureOpenAIEndpoint").value
            self.api_version = client.get_secret("AzureOpenAIVersion").value

            self.initialized = True
            print("✅ Successfully loaded configuration from Key Vault!")
            return True

        except Exception as e:
            print(f"❌ Failed to load from Key Vault: {str(e)}")
            
            print("\n=== AUTHENTICATION FAILED ===")
            print("Please set up authentication in one of these ways:")
            print("1. Set environment variables for direct API access:")
            print("   - AI_API_KEY")
            print("   - AI_ENDPOINT")
            print("   - AI_VERSION")
            print("2. Set environment variables for service principal:")
            print("   - AZURE_CLIENT_ID")
            print("   - AZURE_CLIENT_SECRET")
            print("   - AZURE_TENANT_ID")
            print("=========================\n")
            return False

# Initialize global config
ai_config = AIConfig()

def initialize_app(vault_name):
    """
    Initialize the application configuration with the specified Key Vault name.
    
    Args:
        vault_name (str): The name of your Azure Key Vault instance.
    """
    if not ai_config.initialize(vault_name):
        raise Exception("Failed to initialize configuration")