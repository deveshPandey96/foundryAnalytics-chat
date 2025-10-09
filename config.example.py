"""
Configuration Template for Azure LLM Analytics

Copy this file to config.py and update with your actual credentials.
NEVER commit config.py to version control!
"""

# Azure LLM Endpoint Configuration
AZURE_ENDPOINT_URL = "https://endpointNew-29sep-bdtrm.eastus2.inference.ml.azure.com/score"

# API Key for Authentication
# Replace with your actual API key
API_KEY = "your-api-key-here"

# Default Parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 800

# Chart Configuration
# Note: Chart type can be changed dynamically in the UI
DEFAULT_CHART_TYPE = "bar"  # Options: "bar", "pie", "line", "scatter"
