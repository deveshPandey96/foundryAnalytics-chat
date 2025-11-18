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
    
    def __init__(self, 
                 positive_feedback_file: str = "positive_feedback_log.txt",
                 negative_feedback_file: str = "negative_feedback_log.txt"):
        """
        Initialize feedback logger.
        
        Args:
            positive_feedback_file: Path to the positive feedback log file
            negative_feedback_file: Path to the negative feedback log file
        """
        self.positive_feedback_file = positive_feedback_file
        self.negative_feedback_file = negative_feedback_file
    
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
            
            # Determine which file to write to based on feedback type
            feedback_file = (self.positive_feedback_file if feedback_type == "positive" 
                           else self.negative_feedback_file)
            
            # Append to the appropriate file
            with open(feedback_file, 'a', encoding='utf-8') as f:
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
    
    def _load_feedback(self, feedback_type: str = "all") -> list:
        """
        Load existing feedback from file.
        
        Args:
            feedback_type: Type of feedback to load ("positive", "negative", or "all")
        
        Returns:
            List of feedback entries parsed from TXT format
        """
        files_to_load = []
        
        if feedback_type in ["positive", "all"]:
            if os.path.exists(self.positive_feedback_file):
                files_to_load.append(self.positive_feedback_file)
        
        if feedback_type in ["negative", "all"]:
            if os.path.exists(self.negative_feedback_file):
                files_to_load.append(self.negative_feedback_file)
        
        if not files_to_load:
            return []
        
        try:
            feedback_entries = []
            
            for feedback_file in files_to_load:
                with open(feedback_file, 'r', encoding='utf-8') as f:
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
        positive_entries = self._load_feedback("positive")
        negative_entries = self._load_feedback("negative")
        
        stats = {
            "total": len(positive_entries) + len(negative_entries),
            "positive": len(positive_entries),
            "negative": len(negative_entries)
        }
        
        return stats
    
    def get_feedback_path(self) -> Dict[str, str]:
        """
        Get the absolute paths to the feedback files.
        
        Returns:
            Dictionary with paths to positive and negative feedback files
        """
        return {
            "positive": os.path.abspath(self.positive_feedback_file),
            "negative": os.path.abspath(self.negative_feedback_file)
        }
