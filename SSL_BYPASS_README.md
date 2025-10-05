# SSL Certificate Bypass for Development

## Overview

The `azure_llm_analytics_dev.py` module provides SSL certificate verification bypass functionality for development purposes. This is useful when working with Azure endpoints that have SSL certificate issues during development.

⚠️ **WARNING**: This configuration should **NEVER** be used in production environments as it disables critical security features.

## Changes Made

### 1. SSL Bypass Implementation (`azure_llm_analytics_dev.py`)

The development version includes:
- SSL context that disables certificate verification
- Warnings suppression for SSL-related alerts
- Clear warning messages when the client is initialized

```python
# Create SSL context that doesn't verify certificates (DEVELOPMENT ONLY)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
```

### 2. API Compatibility

To ensure compatibility with `streamlit_dashboard.py`, the `AnalyticsPipeline` class in the development version now includes both:
- `process_query()` - Original method name in dev version
- `run_query()` - New method that matches the production API

This allows seamless switching between production and development versions.

### 3. Dashboard Configuration

The `streamlit_dashboard.py` has been updated to import from the development version:

```python
from azure_llm_analytics_dev import AzureLLMClient, AnalyticsPipeline
```

## Usage

### Running the Dashboard with SSL Bypass

Simply run the Streamlit dashboard as normal:

```bash
streamlit run streamlit_dashboard.py
```

You will see the SSL warning message in the console:
```
⚠️  WARNING: SSL verification is DISABLED for development purposes only!
   Do not use this configuration in production environments.
```

### Switching Between Production and Development

To switch back to the production version with SSL verification:

1. Edit `streamlit_dashboard.py`
2. Change line 8 from:
   ```python
   from azure_llm_analytics_dev import AzureLLMClient, AnalyticsPipeline
   ```
   to:
   ```python
   from azure_llm_analytics import AzureLLMClient, AnalyticsPipeline
   ```

## API Compatibility

Both versions provide the same interface:

```python
client = AzureLLMClient(endpoint_url, api_key)
pipeline = AnalyticsPipeline(client)
result = pipeline.run_query(
    prompt="Your query here",
    temperature=0.7,
    max_tokens=800,
    chart_type="auto"
)
```

The result structure is identical:
```python
{
    'success': bool,
    'response': dict,           # Contains the LLM response
    'extracted_data': list,     # Extracted JSON data
    'chart': plotly.Figure,     # Generated chart (if data extracted)
    'error': str               # Error message (if success=False)
}
```

## Security Considerations

### Why SSL Verification Matters

SSL certificate verification:
- Ensures you're connecting to the correct server
- Prevents man-in-the-middle attacks
- Validates the identity of the endpoint

### When to Use SSL Bypass

SSL bypass should **ONLY** be used:
- ✅ In local development environments
- ✅ With internal/trusted networks
- ✅ When working with self-signed certificates during development
- ✅ Temporarily to diagnose SSL issues

### When NOT to Use SSL Bypass

**NEVER** use SSL bypass:
- ❌ In production environments
- ❌ When handling sensitive data
- ❌ Over public networks
- ❌ As a permanent solution

### Proper Solution for Production

For production environments with SSL certificate issues:
1. Obtain a valid SSL certificate from a trusted Certificate Authority
2. Ensure certificate is properly installed on the Azure endpoint
3. Keep certificates up to date
4. Use the production version (`azure_llm_analytics.py`)

## Testing

The implementation has been tested to ensure:
- ✅ API compatibility with the dashboard
- ✅ Proper error handling
- ✅ SSL warning is displayed
- ✅ Both `run_query()` and `process_query()` methods work
- ✅ Return structures match expected format

## Troubleshooting

### Issue: AttributeError: 'AnalyticsPipeline' object has no attribute 'run_query'

**Solution**: This error occurs when using the old version of `azure_llm_analytics_dev.py`. The current version includes the `run_query()` method.

### Issue: SSL warnings not appearing

**Solution**: This is expected behavior. The warnings module suppresses SSL-related warnings to avoid cluttering the output. The client initialization warning is always shown.

### Issue: Connection still failing with SSL errors

**Solution**: Ensure you're using `azure_llm_analytics_dev` and not `azure_llm_analytics`. Check the import statement in `streamlit_dashboard.py`.

## Support

For issues or questions:
1. Check the warning messages in the console
2. Verify you're using the correct module (dev vs production)
3. Ensure the endpoint URL and API key are correct
4. Review this documentation

---

**Last Updated**: 2025-10-05
**Author**: deveshPandey96
