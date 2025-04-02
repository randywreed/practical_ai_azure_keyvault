from setuptools import setup, find_packages

setup(
    name="practical_ai_azure_keyvault",
    version="0.1.0",
    description="A package for managing Azure OpenAI configuration and authentication.",
    author="Randy Reed",
    author_email="reedrw@appstate.edu",
    url="https://github.com/yourusername/practical_ai_azure_keyvault",
    packages=find_packages(),
    install_requires=[
        "azure-identity",
        "azure-keyvault-secrets",
        "openai"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
