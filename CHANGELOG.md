# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-10-05

### Added
- Added `run_query()` method to `AnalyticsPipeline` in `azure_llm_analytics_dev.py` for API compatibility with the production version
- Created comprehensive SSL bypass documentation (`SSL_BYPASS_README.md`)
- Added SSL certificate issues section to main README
- Enhanced troubleshooting section with SSL-related issues

### Changed
- Updated `streamlit_dashboard.py` to import from `azure_llm_analytics_dev` instead of `azure_llm_analytics` to enable SSL bypass for development
- Modified `azure_llm_analytics_dev.py` to maintain both `process_query()` and `run_query()` methods for backward compatibility

### Fixed
- Fixed `AttributeError: 'AnalyticsPipeline' object has no attribute 'run_query'` when using `azure_llm_analytics_dev` module
- Resolved SSL certificate verification errors in development environments

### Security
- ⚠️ **WARNING**: The application now uses SSL bypass by default via `azure_llm_analytics_dev`. This is intended for development purposes only and should NEVER be used in production environments. See `SSL_BYPASS_README.md` for details.

## Previous Versions

See git history for previous changes.
