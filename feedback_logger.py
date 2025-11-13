"""
Feedback Logger Module

This module provides functionality for logging user feedback on LLM responses:
1. Thumbs up (positive feedback) - silently logs the interaction
2. Thumbs down (negative feedback) - logs with user's preferred answer
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional


class FeedbackLogger:
    """Handles logging of user feedback for LLM responses."""
    
    def __init__(self, feedback_file: str = "feedback_log.json"):
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
            # Load existing feedback
            feedback_entries = self._load_feedback()
            
            # Create new feedback entry
            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "feedback_type": feedback_type,
                "query": query,
                "model_response": response,
                "extracted_data": extracted_data,
                "metadata": metadata or {}
            }
            
            # Add preferred answer for negative feedback
            if feedback_type == "negative" and preferred_answer:
                feedback_entry["preferred_answer"] = preferred_answer
            
            # Append new entry
            feedback_entries.append(feedback_entry)
            
            # Save to file
            with open(self.feedback_file, 'w', encoding='utf-8') as f:
                json.dump(feedback_entries, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error logging feedback: {e}")
            return False
    
    def _load_feedback(self) -> list:
        """
        Load existing feedback from file.
        
        Returns:
            List of feedback entries
        """
        if not os.path.exists(self.feedback_file):
            return []
        
        try:
            with open(self.feedback_file, 'r', encoding='utf-8') as f:
                return json.load(f)
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
        
        stats = {
            "total": len(feedback_entries),
            "positive": sum(1 for entry in feedback_entries if entry.get("feedback_type") == "positive"),
            "negative": sum(1 for entry in feedback_entries if entry.get("feedback_type") == "negative")
        }
        
        return stats
    
    def get_feedback_path(self) -> str:
        """
        Get the absolute path to the feedback file.
        
        Returns:
            Absolute path to feedback file
        """
        return os.path.abspath(self.feedback_file)
