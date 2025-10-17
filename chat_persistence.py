"""
Chat Persistence and Logging Module

This module provides functionality for:
1. Persisting chat history to a local file (survives page refresh)
2. Logging all queries and responses to a log file
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import plotly.graph_objects as go


class ChatPersistence:
    """Handles chat history persistence to local storage."""
    
    def __init__(self, history_file: str = "chat_history.json"):
        """
        Initialize chat persistence handler.
        
        Args:
            history_file: Path to the history file
        """
        self.history_file = history_file
    
    def save_history(self, chat_history: List[Dict[str, Any]]) -> bool:
        """
        Save chat history to file.
        
        Args:
            chat_history: List of chat entries
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create a serializable version of history
            serializable_history = []
            
            for entry in chat_history:
                serializable_entry = {
                    'query': entry.get('query', ''),
                    'text_response': entry.get('text_response', ''),
                    'extracted_data': entry.get('extracted_data'),
                    'chart_type': entry.get('chart_type', 'bar'),
                    'has_data': entry.get('has_data', False),
                    'raw_response': entry.get('raw_response', ''),
                    'timestamp': entry.get('timestamp', datetime.now().isoformat())
                }
                
                # Handle Plotly chart - convert to JSON
                if entry.get('chart'):
                    try:
                        chart_json = entry['chart'].to_json()
                        serializable_entry['chart_json'] = chart_json
                    except:
                        serializable_entry['chart_json'] = None
                else:
                    serializable_entry['chart_json'] = None
                
                serializable_history.append(serializable_entry)
            
            # Write to file
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_history, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving chat history: {e}")
            return False
    
    def load_history(self) -> List[Dict[str, Any]]:
        """
        Load chat history from file.
        
        Returns:
            List of chat entries, empty list if file doesn't exist or error occurs
        """
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                serializable_history = json.load(f)
            
            # Convert back to chat history format
            chat_history = []
            
            for entry in serializable_history:
                chat_entry = {
                    'query': entry.get('query', ''),
                    'text_response': entry.get('text_response', ''),
                    'extracted_data': entry.get('extracted_data'),
                    'chart_type': entry.get('chart_type', 'bar'),
                    'has_data': entry.get('has_data', False),
                    'raw_response': entry.get('raw_response', ''),
                    'timestamp': entry.get('timestamp', datetime.now().isoformat())
                }
                
                # Reconstruct Plotly chart from JSON
                if entry.get('chart_json'):
                    try:
                        chart = go.Figure(json.loads(entry['chart_json']))
                        chat_entry['chart'] = chart
                    except:
                        chat_entry['chart'] = None
                else:
                    chat_entry['chart'] = None
                
                chat_history.append(chat_entry)
            
            return chat_history
            
        except Exception as e:
            print(f"Error loading chat history: {e}")
            return []
    
    def clear_history(self) -> bool:
        """
        Clear chat history file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            return True
        except Exception as e:
            print(f"Error clearing chat history: {e}")
            return False


class QueryLogger:
    """Handles logging of queries and responses to a log file."""
    
    def __init__(self, log_file: str = "query_log.txt"):
        """
        Initialize query logger.
        
        Args:
            log_file: Path to the log file
        """
        self.log_file = log_file
    
    def log_query(
        self, 
        query: str, 
        response: str, 
        extracted_data: Optional[List[Dict[str, Any]]] = None,
        success: bool = True
    ) -> bool:
        """
        Log a query and its response to file.
        
        Args:
            query: The user's query
            response: The LLM's response
            extracted_data: Extracted structured data (if any)
            success: Whether the query was successful
            
        Returns:
            True if successful, False otherwise
        """
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Format log entry
            log_entry = f"""
{'='*80}
TIMESTAMP: {timestamp}
STATUS: {'SUCCESS' if success else 'FAILED'}

QUERY:
{query}

RESPONSE:
{response}
"""
            
            # Add extracted data if available
            if extracted_data:
                log_entry += f"""
EXTRACTED DATA:
{json.dumps(extracted_data, indent=2, ensure_ascii=False)}
"""
            
            log_entry += f"{'='*80}\n\n"
            
            # Append to log file
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            return True
            
        except Exception as e:
            print(f"Error logging query: {e}")
            return False
    
    def get_log_path(self) -> str:
        """
        Get the absolute path to the log file.
        
        Returns:
            Absolute path to log file
        """
        return os.path.abspath(self.log_file)
