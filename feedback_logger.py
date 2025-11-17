"""
Feedback Logger Module

This module provides functionality for logging user feedback on LLM responses:
1. Thumbs up (positive feedback) - silently logs the interaction
2. Thumbs down (negative feedback) - logs with user's preferred answer
"""

import os
from datetime import datetime
from typing import Dict, Any, Optional


class FeedbackLogger:
    """Handles logging of user feedback for LLM responses."""
    
    def __init__(self, feedback_file: str = "feedback_log.txt"):
        """
        Initialize feedback logger.
        
        Args:
            feedback_file: Path to the feedback log file
        """
        self.feedback_file = feedback_file
    
    def log_feedback(
        self, 
        query: str,
        response: str,
        feedback_type: str,
        extracted_data: Optional[Any] = None,
        preferred_answer: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Log user feedback for a query-response pair.
        
        Args:
            query: The user's query
            response: The LLM's response
            feedback_type: Type of feedback ("positive" or "negative")
            extracted_data: Extracted structured data (if any)
            preferred_answer: User's preferred answer (for negative feedback)
            metadata: Additional metadata to log
            
        Returns:
            True if successful, False otherwise
        """
        try:
            timestamp = datetime.now().isoformat()
            
            # For negative feedback with preferred answer, log it
            # For positive feedback, we use the model response
            if feedback_type == "negative" and preferred_answer:
                response_text = preferred_answer
            else:
                response_text = response
            
            # Format the log entry
            log_entry = self._format_log_entry(timestamp, query, response_text)
            
            # Append to file
            with open(self.feedback_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            return True
            
        except Exception as e:
            print(f"Error logging feedback: {e}")
            return False
    
    def _format_log_entry(self, timestamp: str, query: str, response: str) -> str:
        """
        Format a log entry in the specified text format.
        
        Args:
            timestamp: ISO format timestamp
            query: The user's query
            response: The response text (model response or preferred answer)
            
        Returns:
            Formatted log entry string
        """
        separator = "=" * 80
        entry = f"{separator}\n"
        entry += f"TIMESTAMP: {timestamp}\n"
        entry += f"STATUS: SUCCESS\n\n"
        entry += f"QUERY:\n{query}\n\n"
        entry += f"RESPONSE:\n{response}\n"
        entry += f"{separator}\n\n"
        return entry
    
    def _load_feedback(self) -> list:
        """
        Load existing feedback from file.
        
        Returns:
            List of feedback entries parsed from TXT format
        """
        if not os.path.exists(self.feedback_file):
            return []
        
        try:
            feedback_entries = []
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by separator lines
            separator = "=" * 80
            entries = content.split(separator)
            
            for entry in entries:
                entry = entry.strip()
                if not entry:
                    continue
                
                # Parse each entry
                lines = entry.split('\n')
                parsed_entry = {}
                
                # Extract timestamp
                for line in lines:
                    if line.startswith("TIMESTAMP:"):
                        parsed_entry["timestamp"] = line.replace("TIMESTAMP:", "").strip()
                        break
                
                # Extract query
                if "QUERY:" in entry:
                    query_start = entry.find("QUERY:") + len("QUERY:")
                    query_end = entry.find("RESPONSE:")
                    if query_end > query_start:
                        parsed_entry["query"] = entry[query_start:query_end].strip()
                
                # Extract response
                if "RESPONSE:" in entry:
                    response_start = entry.find("RESPONSE:") + len("RESPONSE:")
                    parsed_entry["response"] = entry[response_start:].strip()
                
                if parsed_entry:
                    feedback_entries.append(parsed_entry)
            
            return feedback_entries
            
        except Exception as e:
            print(f"Error loading feedback: {e}")
            return []
    
    def get_feedback_stats(self) -> Dict[str, int]:
        """
        Get statistics on feedback.
        
        Returns:
            Dictionary with feedback counts
        """
        feedback_entries = self._load_feedback()
        
        # In the new TXT format, we don't distinguish between positive/negative
        # All logged entries are counted as total feedback
        stats = {
            "total": len(feedback_entries),
            "positive": 0,  # Not tracked in new format
            "negative": 0   # Not tracked in new format
        }
        
        return stats
    
    def get_feedback_path(self) -> str:
        """
        Get the absolute path to the feedback file.
        
        Returns:
            Absolute path to feedback file
        """
        return os.path.abspath(self.feedback_file)
