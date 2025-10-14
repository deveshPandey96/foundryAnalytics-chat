# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased] - 2025-10-14

### Added - Chat-like UI 🎨
- **Conversational Interface**: Implemented chat-like UI similar to ChatGPT/Copilot using Streamlit's `st.chat_message()`
- **Chat History**: Added persistent conversation history throughout the session
- **Smart Text Rendering**: Created `extract_readable_text()` function to convert JSON responses to natural language summaries
- **Dual-View Tabs**: Each response now has "Detailed Response" and "Graph View" tabs inline with the message
- **Dynamic Chart Selection**: Users can switch chart types (bar, pie, line, scatter) per response
- **Custom CSS Styling**: Added rounded corners and chat-like visual styling
- **Clear Chat Button**: Added ability to reset conversation and start fresh

### Changed
- **Input Field**: Changed from multi-line `text_area` to single-line `text_input` for better chat UX
- **Response Display**: Responses now show narrative summaries instead of raw JSON by default
- **Layout**: Conversation history now appears above the input field, following chat app conventions
- **Documentation**: Updated README with new UI features and screenshot

### Improved
- **User Experience**: More intuitive, familiar interface for users accustomed to modern chat applications
- **Data Readability**: JSON data automatically converted to bullet-point summaries with totals
- **Context Preservation**: All previous queries and responses remain visible and accessible
- **Visualization Flexibility**: Chart types can be changed independently for each message in history

## [2025-10-05]

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
