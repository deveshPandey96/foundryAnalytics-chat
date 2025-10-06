"""
Azure LLM Analytics Client and Visualization Module

This module provides a client to interact with Azure LLM endpoints
and utilities to extract JSON data and create visualizations.
"""

import json
import urllib.request
import urllib.error
import re
from typing import Dict, Any, Optional, List, Tuple
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


class AzureLLMClient:
    """Client for interacting with Azure LLM endpoint."""
    
    def __init__(self, endpoint_url: str, api_key: str):
        """
        Initialize the Azure LLM client.
        
        Args:
            endpoint_url: Azure endpoint URL
            api_key: API key for authentication
        """
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        
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
            # Send request
            with urllib.request.urlopen(req, timeout=30) as response:
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
            return True, "Connection successful!"
        else:
            return False, f"Connection failed: {result.get('error', 'Unknown error')}"


class JSONExtractor:
    """Utility class to extract JSON data from LLM responses."""
    
    @staticmethod
    def extract_json(text: str) -> Optional[List[Dict[str, Any]]]:
        """
        Extract JSON data from text response.
        
        This method tries multiple strategies to find and parse JSON:
        1. Direct JSON parsing
        2. Extracting JSON from code blocks
        3. Finding JSON arrays or objects in text
        
        Args:
            text: Text containing JSON data
            
        Returns:
            List of dictionaries if JSON found, None otherwise
        """
        if not text:
            return None
            
        # Strategy 1: Try direct parsing
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return parsed
            elif isinstance(parsed, dict):
                return [parsed]
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Extract from code blocks (```json ... ```)
        json_blocks = re.findall(r'```(?:json)?\s*(\[.*?\]|\{.*?\})\s*```', text, re.DOTALL)
        for block in json_blocks:
            try:
                parsed = json.loads(block)
                if isinstance(parsed, list):
                    return parsed
                elif isinstance(parsed, dict):
                    return [parsed]
            except json.JSONDecodeError:
                continue
        
        # Strategy 3: Find JSON array or object anywhere in text
        # Look for arrays
        array_matches = re.findall(r'\[\s*\{.*?\}\s*(?:,\s*\{.*?\}\s*)*\]', text, re.DOTALL)
        for match in array_matches:
            try:
                parsed = json.loads(match)
                if isinstance(parsed, list):
                    return parsed
            except json.JSONDecodeError:
                continue
        
        # Look for single objects
        object_matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text)
        for match in object_matches:
            try:
                parsed = json.loads(match)
                if isinstance(parsed, dict):
                    return [parsed]
            except json.JSONDecodeError:
                continue
        
        return None
    
    @staticmethod
    def extract_from_response(response: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        Extract JSON from Azure LLM response.
        
        Args:
            response: Response dictionary from query method
            
        Returns:
            List of dictionaries if JSON found, None otherwise
        """
        if not response.get('success'):
            return None
        
        # Try to extract from different possible response structures
        response_data = response.get('response', {})
        
        # Check common response fields
        possible_fields = ['output', 'result', 'data', 'content', 'text', 'message']
        
        for field in possible_fields:
            if field in response_data:
                text = str(response_data[field])
                extracted = JSONExtractor.extract_json(text)
                if extracted:
                    return extracted
        
        # Try the raw response as string
        raw_text = response.get('raw_text', '')
        return JSONExtractor.extract_json(raw_text)


class ChartGenerator:
    """Generate interactive charts from data."""
    
    @staticmethod
    def create_bar_chart(data: List[Dict[str, Any]], x_key: str, y_key: str, title: str = "Bar Chart") -> go.Figure:
        """
        Create a bar chart from data.
        
        Args:
            data: List of dictionaries containing data
            x_key: Key for x-axis values
            y_key: Key for y-axis values
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        df = pd.DataFrame(data)
        
        fig = go.Figure(data=[
            go.Bar(
                x=df[x_key],
                y=df[y_key],
                text=df[y_key],
                textposition='auto',
                marker_color='rgb(55, 83, 109)'
            )
        ])
        
        fig.update_layout(
            title=title,
            xaxis_title=x_key.capitalize(),
            yaxis_title=y_key.capitalize(),
            template='plotly_white',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_pie_chart(data: List[Dict[str, Any]], labels_key: str, values_key: str, title: str = "Pie Chart") -> go.Figure:
        """
        Create a pie chart from data.
        
        Args:
            data: List of dictionaries containing data
            labels_key: Key for label values
            values_key: Key for numeric values
            title: Chart title
            
        Returns:
            Plotly figure object
        """
        df = pd.DataFrame(data)
        
        fig = go.Figure(data=[
            go.Pie(
                labels=df[labels_key],
                values=df[values_key],
                hole=0.3,
                textinfo='label+percent',
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title=title,
            template='plotly_white'
        )
        
        return fig
    
    @staticmethod
    def auto_generate_chart(data: List[Dict[str, Any]], chart_type: str = "auto") -> Optional[go.Figure]:
        """
        Automatically generate an appropriate chart based on data structure.
        
        Args:
            data: List of dictionaries containing data
            chart_type: Type of chart ('auto', 'bar', 'pie')
            
        Returns:
            Plotly figure object or None if unable to generate
        """
        if not data:
            return None
        
        df = pd.DataFrame(data)
        
        if len(df.columns) < 2:
            return None
        
        # Identify categorical and numeric columns
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not categorical_cols or not numeric_cols:
            # Try to convert first column to categorical and second to numeric
            cols = df.columns.tolist()
            if len(cols) >= 2:
                categorical_cols = [cols[0]]
                try:
                    df[cols[1]] = pd.to_numeric(df[cols[1]])
                    numeric_cols = [cols[1]]
                except:
                    return None
        
        if not categorical_cols or not numeric_cols:
            return None
        
        cat_col = categorical_cols[0]
        num_col = numeric_cols[0]
        
        # Determine chart type
        if chart_type == "auto":
            # Use bar chart for most cases
            chart_type = "bar"
        
        if chart_type == "bar":
            return ChartGenerator.create_bar_chart(
                data, cat_col, num_col,
                title=f"{num_col.capitalize()} by {cat_col.capitalize()}"
            )
        elif chart_type == "pie":
            return ChartGenerator.create_pie_chart(
                data, cat_col, num_col,
                title=f"{num_col.capitalize()} Distribution"
            )
        
        return None


class AnalyticsPipeline:
    """Complete pipeline for querying, extracting, and visualizing data."""
    
    def __init__(self, client: AzureLLMClient):
        """
        Initialize the analytics pipeline.
        
        Args:
            client: AzureLLMClient instance
        """
        self.client = client
        self.extractor = JSONExtractor()
        self.chart_generator = ChartGenerator()
    
    def run_query(
        self, 
        prompt: str, 
        temperature: float = 0.7, 
        max_tokens: int = 800,
        chart_type: str = "auto"
    ) -> Dict[str, Any]:
        """
        Run complete analytics pipeline: query -> extract -> visualize.
        
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
        
        # Extract JSON data
        extracted_data = self.extractor.extract_from_response(response)
        
        result = {
            'success': True,
            'response': response,
            'extracted_data': extracted_data,
            'chart': None
        }
        
        # Generate chart if data was extracted
        if extracted_data:
            try:
                chart = self.chart_generator.auto_generate_chart(extracted_data, chart_type)
                result['chart'] = chart
            except Exception as e:
                result['chart_error'] = str(e)
        
        return result
