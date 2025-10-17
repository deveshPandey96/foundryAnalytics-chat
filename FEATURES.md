# New Features: Chat History Persistence & Query Logging

## Overview

Two new powerful features have been added to the Azure LLM Analytics Dashboard to improve user experience and data tracking:

1. **Chat History Persistence** - Retain your conversation history even after refreshing the page
2. **Query Logging** - Automatically log all queries and responses to a local file

## Feature 1: Chat History Persistence

### What It Does
- Automatically saves your entire chat history to a local JSON file (`chat_history.json`)
- Loads previous conversations when you restart the application
- Preserves all data including queries, responses, extracted data, and charts
- Survives browser refresh, app restart, and system reboot

### How It Works
- History is automatically saved after each new query
- When you open the dashboard, it checks for existing history and loads it
- A success message appears when history is restored
- The sidebar shows the total number of saved conversations

### User Experience
1. **Automatic Save**: Every time you submit a query, your conversation is saved
2. **Automatic Restore**: When you refresh or reopen the dashboard, your chat history appears automatically
3. **Success Notification**: You'll see "✅ Chat history restored! Loaded X previous conversation(s)." when history is loaded
4. **Clear History**: The "Clear Chat" button clears both the current session and the persisted file

### File Location
- **File**: `chat_history.json` (in the root directory of the application)
- **Format**: JSON with full conversation details
- **Excluded from Git**: Added to `.gitignore` to prevent accidental commits

### Example Chat History JSON Structure
```json
[
  {
    "query": "Compare tasks in phase 3 and phase 6",
    "text_response": "Phase 3 has 10 tasks, Phase 6 has 15 tasks",
    "extracted_data": [
      {"phase": "Phase 3", "tasks": 10},
      {"phase": "Phase 6", "tasks": 15}
    ],
    "chart_type": "bar",
    "has_data": true,
    "raw_response": "...",
    "timestamp": "2025-10-17T04:21:52.378551",
    "chart_json": "{...}"
  }
]
```

## Feature 2: Query Logging

### What It Does
- Logs every query and response to a human-readable text file (`query_log.txt`)
- Includes timestamps, status (SUCCESS/FAILED), and extracted data
- Provides a permanent record of all interactions with the LLM
- Useful for debugging, auditing, and analysis

### How It Works
- Every time you submit a query, it's logged along with the response
- Both successful and failed queries are logged
- Extracted structured data is included in JSON format when available
- Each log entry is clearly separated and timestamped

### User Experience
1. **Automatic Logging**: All queries are logged without any user action required
2. **Sidebar Info**: The sidebar shows the location of the log file
3. **Status Tracking**: Each log entry shows whether the query succeeded or failed
4. **Data Preservation**: Complete query history is preserved even if chat history is cleared

### File Location
- **File**: `query_log.txt` (in the root directory of the application)
- **Format**: Human-readable text with clear separators
- **Excluded from Git**: Added to `.gitignore` to prevent accidental commits

### Example Log Entry Format
```
================================================================================
TIMESTAMP: 2025-10-17 04:21:52
STATUS: SUCCESS

QUERY:
Compare the number of tasks in phase 3 and phase 6

RESPONSE:
According to the data, Phase 3 has 10 tasks and Phase 6 has 15 tasks.

EXTRACTED DATA:
[
  {
    "phase": "Phase 3",
    "tasks": 10
  },
  {
    "phase": "Phase 6",
    "tasks": 15
  }
]
================================================================================
```

## Sidebar Information

The sidebar now includes a "📝 Logging Info" section showing:
- Status of automatic saving
- Location of log files (`query_log.txt` and `chat_history.json`)
- Total number of conversations in history

## Technical Details

### New Module: `chat_persistence.py`

This module contains two main classes:

#### `ChatPersistence`
- `save_history(chat_history)`: Saves chat history to JSON file
- `load_history()`: Loads chat history from JSON file
- `clear_history()`: Clears the persisted history file
- Handles Plotly chart serialization/deserialization

#### `QueryLogger`
- `log_query(query, response, extracted_data, success)`: Logs a query and response
- `get_log_path()`: Returns the absolute path to the log file
- Creates human-readable log entries with timestamps

### Integration with Streamlit Dashboard

The `streamlit_dashboard.py` has been updated to:
1. Import and initialize the persistence and logging modules
2. Load chat history on startup
3. Save history after each query
4. Log all queries and responses
5. Display restore notification
6. Update sidebar with logging information
7. Clear persisted files when "Clear Chat" is clicked

## Files Modified

1. **`streamlit_dashboard.py`** - Main dashboard file
   - Added imports for persistence module
   - Initialized persistence and logging
   - Added history loading on startup
   - Added saving after each query
   - Added logging for all queries
   - Updated sidebar with logging info

2. **`.gitignore`** - Git ignore file
   - Added `query_log.txt` to prevent committing logs
   - Added `chat_history.json` to prevent committing history

3. **`chat_persistence.py`** - New module (created)
   - Implements ChatPersistence class
   - Implements QueryLogger class

## Benefits

### For Users
- **Convenience**: No need to worry about losing your work when you refresh the page
- **Continuity**: Pick up where you left off without re-entering queries
- **Audit Trail**: Complete log of all interactions for reference

### For Developers
- **Debugging**: Easy access to query logs for troubleshooting
- **Analysis**: Historical data for understanding usage patterns
- **Testing**: Preserved conversations for testing and validation

## Privacy & Security

- **Local Storage**: All data is stored locally on your machine
- **No Cloud Sync**: History and logs are not sent to any external servers
- **Git Excluded**: Files are automatically excluded from version control
- **User Control**: Clear Chat button removes all persisted data

## Usage Tips

1. **Regular Backups**: Consider backing up your `query_log.txt` and `chat_history.json` files periodically
2. **Clear When Needed**: Use the Clear Chat button to remove old conversations and start fresh
3. **Review Logs**: Check `query_log.txt` to review your query history or debug issues
4. **Disk Space**: Monitor log file size if you run many queries (log file grows over time)

## Future Enhancements

Potential improvements for future versions:
- Export chat history to different formats (CSV, PDF)
- Search functionality within chat history
- Log rotation to manage file size
- Cloud backup options
- History import/export

## Support

If you encounter any issues with these features:
1. Check that the application has write permissions in its directory
2. Verify that `chat_history.json` and `query_log.txt` are not locked by another process
3. Check the Streamlit console for any error messages
4. Review the troubleshooting section in the main README

---

**Last Updated**: October 17, 2025  
**Version**: 2.0
