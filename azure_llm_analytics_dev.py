"""
Azure LLM Analytics Client and Visualization Module - Development Version

This module provides a client to interact with Azure LLM endpoints
with SSL verification disabled for development purposes.
"""

import json
import urllib.request
import urllib.error
import ssl
import re
from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# Create SSL context that doesn't verify certificates (DEVELOPMENT ONLY)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Disable SSL warnings for development
import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')


class AzureLLMClient:
    """Client for interacting with Azure LLM endpoint with SSL verification disabled."""
    
    def __init__(self, endpoint_url: str, api_key: str):
        """
        Initialize the Azure LLM client.
        
        Args:
            endpoint_url: Azure endpoint URL
            api_key: API key for authentication
        """
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        print("⚠️  WARNING: SSL verification is DISABLED for development purposes only!")
        print("   Do not use this configuration in production environments.")
        
    def query(
        self, 
        prompt: str, 
        temperature: float = 0.7, 
        max_tokens: int = 800
    ) -> Dict[str, Any]:
        """
        Send a query to the Azure LLM endpoint.
        
        Args:
            prompt: The query/prompt to send
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            Dictionary containing the response and metadata
            
        Raises:
            urllib.error.URLError: If connection fails
            ValueError: If response is invalid
        """
        # Prepare the request data
        data = {
            "chat_input": prompt,
            "chat_history": []
        }
        
        # Convert to JSON and encode
        body = json.dumps(data).encode('utf-8')
        
        # Prepare headers
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        # Create request
        req = urllib.request.Request(
            self.endpoint_url,
            data=body,
            headers=headers,
            method='POST'
        )
        
        try:
            # Send request with SSL verification disabled
            with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
                response_data = response.read().decode('utf-8')
                result = json.loads(response_data)
                
                return {
                    'success': True,
                    'response': result,
                    'raw_text': result.get('chat_output', str(result))
                }
                
        except urllib.error.HTTPError as e:
            error_message = e.read().decode('utf-8') if e.fp else str(e)
            return {
                'success': False,
                'error': f'HTTP Error {e.code}: {error_message}',
                'status_code': e.code
            }
            
        except urllib.error.URLError as e:
            return {
                'success': False,
                'error': f'Connection Error: {str(e.reason)}'
            }
            
        except json.JSONDecodeError as e:
            return {
                'success': False,
                'error': f'Invalid JSON response: {str(e)}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def test_connection(self) -> Tuple[bool, str]:
        """
        Test the connection to the Azure endpoint.
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        result = self.query("Hello, this is a connection test.", temperature=0.5, max_tokens=50)
        
        if result['success']:
            return True, "✅ Connection successful!"
        else:
            return False, f"❌ Connection failed: {result['error']}"


class AnalyticsPipeline:
    """Pipeline for processing LLM responses and creating visualizations."""
    
    def __init__(self, client: AzureLLMClient):
        """
        Initialize the analytics pipeline.
        
        Args:
            client: AzureLLMClient instance
        """
        self.client = client
    
    def extract_json(self, text: str) -> Optional[List[Dict[str, Any]]]:
        """
        Extract JSON data from LLM response text.
        
        Args:
            text: Text containing JSON data
            
        Returns:
            List of dictionaries if JSON found, None otherwise
        """
        # Multiple patterns to find JSON in text
        json_patterns = [
            r'```json\s*(\[.*?\])\s*```',  # JSON in code blocks
            r'```\s*(\[.*?\])\s*```',      # JSON in generic code blocks
            r'(\[.*?\])',                   # Raw JSON arrays
            r'(\{.*?\})'                    # Raw JSON objects
        ]
        
        for pattern in json_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                try:
                    data = json.loads(match)
                    # Convert single object to list
                    if isinstance(data, dict):
                        return [data]
                    elif isinstance(data, list):
                        return data
                except json.JSONDecodeError:
                    continue
        
        return None
    
    def create_chart(
        self, 
        data: List[Dict[str, Any]], 
        chart_type: str = "auto"
    ) -> Optional[go.Figure]:
        """
        Create a chart from the extracted data.
        
        Args:
            data: List of dictionaries containing the data
            chart_type: Type of chart ("auto", "bar", "pie")
            
        Returns:
            Plotly figure object or None if creation fails
        """
        if not data:
            return None
        
        try:
            df = pd.DataFrame(data)
            
            # Determine columns
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(text_cols) == 0 or len(numeric_cols) == 0:
                return None
            
            x_col = text_cols[0]
            y_col = numeric_cols[0]
            
            # Auto-detect chart type if needed
            if chart_type == "auto":
                if len(data) <= 5:
                    chart_type = "pie"
                else:
                    chart_type = "bar"
            
            # Create chart based on type
            if chart_type == "pie":
                fig = px.pie(
                    df, 
                    values=y_col, 
                    names=x_col,
                    title=f"{y_col.title()} by {x_col.title()}"
                )
            else:  # bar chart
                fig = px.bar(
                    df, 
                    x=x_col, 
                    y=y_col,
                    title=f"{y_col.title()} by {x_col.title()}"
                )
                fig.update_layout(
                    xaxis_title=x_col.title(),
                    yaxis_title=y_col.title()
                )
            
            fig.update_layout(
                font_size=12,
                title_font_size=16,
                height=500
            )
            
            return fig
            
        except Exception as e:
            print(f"Error creating chart: {e}")
            return None
    
    def process_query(
        self, 
        prompt: str, 
        temperature: float = 0.7, 
        max_tokens: int = 800,
        chart_type: str = "auto"
    ) -> Dict[str, Any]:
        """
        Process a query end-to-end: send to LLM, extract JSON, create chart.
        
        Args:
            prompt: The query to send
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            chart_type: Type of chart to create
            
        Returns:
            Dictionary with results including chart and extracted data
        """
        # Query the LLM
        llm_result = self.client.query(prompt, temperature, max_tokens)
        
        if not llm_result['success']:
            return {
                'success': False,
                'error': llm_result['error'],
                'llm_response': None,
                'extracted_data': None,
                'chart': None
            }
        
        # Extract JSON from response
        response_text = llm_result['raw_text']
        extracted_data = self.extract_json(response_text)
        
        # Create chart if data was extracted
        chart = None
        if extracted_data:
            chart = self.create_chart(extracted_data, chart_type)
        
        return {
            'success': True,
            'llm_response': llm_result['response'],
            'raw_response': response_text,
            'extracted_data': extracted_data,
            'chart': chart,
            'data_found': extracted_data is not None,
            'chart_created': chart is not None
        }
    
    def run_query(
        self, 
        prompt: str, 
        temperature: float = 0.7, 
        max_tokens: int = 800,
        chart_type: str = "auto"
    ) -> Dict[str, Any]:
        """
        Run complete analytics pipeline: query -> extract -> visualize.
        
        This method wraps process_query() and returns a structure compatible
        with the production version for use with streamlit_dashboard.py.
        
        Args:
            prompt: Query prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            chart_type: Type of chart to generate
            
        Returns:
            Dictionary with response, extracted data, and chart
        """
        # Query the LLM
        response = self.client.query(prompt, temperature, max_tokens)
        
        if not response['success']:
            return response
        
        # Extract JSON from response
        extracted_data = self.extract_json(response['raw_text'])
        
        result = {
            'success': True,
            'response': response,
            'extracted_data': extracted_data,
            'chart': None
        }
        
        # Generate chart if data was extracted
        if extracted_data:
            try:
                chart = self.create_chart(extracted_data, chart_type)
                result['chart'] = chart
            except Exception as e:
                result['chart_error'] = str(e)
        
        return result