# Azure LLM Analytics Dashboard 📊

A production-ready Python application for querying Azure LLM endpoints and automatically visualizing JSON responses. Perfect for comparative analysis, data exploration, and generating interactive charts from natural language queries.

## 🎨 Chat-like UI

The dashboard now features a modern, conversational interface similar to ChatGPT and GitHub Copilot:

![Chat UI Demo](https://github.com/user-attachments/assets/042876aa-24c0-4f20-80b0-d18bee3a6733)

### Key UI Improvements:
- 💬 **Conversation-style layout** with clear user/assistant messages
- 📝 **Natural language summaries** instead of raw JSON display
- 📊 **Inline tabs** for detailed data and visualizations
- 🔄 **Persistent chat history** throughout your session
- 🎯 **Clean, minimal input field** for easy query entry

## Features ✨

- **Chat-like Interface**: Modern conversational UI similar to ChatGPT/Copilot for natural interactions
- **Conversation History**: Keep track of all your queries and responses in one place
- **Smart Text Rendering**: Automatically converts JSON responses to readable text summaries
- **Azure LLM Integration**: Connect to Azure LLM endpoints with Bearer token authentication
- **Automatic JSON Extraction**: Intelligently extracts structured data from LLM responses
- **Interactive Visualizations**: Generate bar charts, pie charts, line charts, and scatter plots using Plotly
- **Dual-View Tabs**: View detailed data and graphs side-by-side within each response
- **Configuration Management**: Easy setup with configuration templates
- **Example Queries**: Pre-loaded analytical queries for quick start
- **Error Handling**: Robust error handling and user feedback
- **Customizable Parameters**: Adjust temperature, max_tokens, and chart types

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Azure LLM endpoint access and API key

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/deveshPandey96/foundryAnalytics-chat.git
   cd foundryAnalytics-chat
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your credentials**
   ```bash
   # Copy the example config file
   cp config.example.py config.py
   
   # Edit config.py and add your API key
   # IMPORTANT: Never commit config.py to version control!
   ```

## SSL Certificate Issues (Development) 🔒

If you encounter SSL certificate verification errors when connecting to your Azure endpoint, a development version with SSL bypass is available:

⚠️ **WARNING**: This should **ONLY** be used in development environments. **NEVER** use this in production!

The repository includes `azure_llm_analytics_dev.py` which has SSL verification disabled. The dashboard is currently configured to use this version for development purposes.

**Current Configuration**: The `streamlit_dashboard.py` imports from `azure_llm_analytics_dev` (development version with SSL bypass).

To switch back to the production version with SSL verification enabled:
1. Edit `streamlit_dashboard.py`
2. Change line 8 from `from azure_llm_analytics_dev import` to `from azure_llm_analytics import`

For detailed information about SSL bypass, security considerations, and troubleshooting, see [SSL_BYPASS_README.md](SSL_BYPASS_README.md).

## Usage 📖

### Running the Streamlit Dashboard

The easiest way to use the application is through the interactive web dashboard:

```bash
streamlit run streamlit_dashboard.py
```

This will launch the dashboard in your default web browser (typically at `http://localhost:8501`).

#### Dashboard Features:

1. **Chat-like Conversation View** 🆕
   - View all your previous queries and responses in a conversation format
   - User messages and assistant responses clearly distinguished
   - Scroll through your complete conversation history
   - Each response shows a natural language summary of the data

2. **Smart Response Rendering** 🆕
   - JSON responses automatically converted to readable text
   - Bullet-point summaries with key insights
   - Total calculations displayed when applicable
   - Clean, chat-like presentation similar to ChatGPT

3. **Interactive Tabs for Each Response** 🆕
   - **Detailed Response Tab**: View extracted data in table format with download options
   - **Graph View Tab**: Interactive Plotly charts with dynamic chart type selection
   - Switch between bar, pie, line, and scatter charts on the fly

4. **Query Input**
   - Clean, single-line input field for queries
   - Pre-loaded example queries for quick start
   - Submit button to send queries
   - Clear Chat button to start a new conversation

5. **Tips Sidebar**
   - Helpful tips for writing effective queries
   - Best practices for getting JSON responses
   - Visualization recommendations

### Using the Python API

You can also use the modules programmatically:

```python
from azure_llm_analytics import AzureLLMClient, AnalyticsPipeline

# Initialize client
client = AzureLLMClient(
    endpoint_url="https://your-endpoint.azure.com/score",
    api_key="your-api-key"
)

# Test connection
success, message = client.test_connection()
print(message)

# Create pipeline
pipeline = AnalyticsPipeline(client)

# Run a query
result = pipeline.run_query(
    prompt="Compare the number of tasks in phase 3 and phase 6. Return as JSON with 'phase' and 'tasks' keys.",
    temperature=0.7,
    max_tokens=800,
    chart_type="bar"
)

# Access results
if result['success']:
    print("Extracted Data:", result['extracted_data'])
    if result['chart']:
        result['chart'].show()  # Display the chart
```

### Running Example Queries

The `examples/sample_queries.py` file contains pre-configured example queries:

```bash
cd examples
python sample_queries.py
```

This will:
1. Test the connection to your Azure endpoint
2. List all available example queries
3. Run the first example query

To run a specific example:
```bash
python sample_queries.py 2  # Runs example #2
```

## Example Queries 💡

Here are some example queries that work well with this system:

1. **Phase Comparison**
   ```
   Compare the number of tasks in phase 3 and phase 6 of J&K Bank. 
   Return the result in JSON format with 'phase' and 'tasks' keys.
   ```

2. **Use Cases Comparison**
   ```
   Compare number of use cases of CSB bank and J&K Bank. 
   Return the result in JSON format with 'customer' and 'use cases' keys.
   ```

3. **Quarterly Revenue**
   ```
   Show the quarterly revenue for Q1, Q2, Q3, and Q4. 
   Return as JSON with 'quarter' and 'revenue' keys.
   ```

4. **Department Headcount**
   ```
   Compare the number of employees in Engineering, Sales, and Marketing departments. 
   Return as JSON with 'department' and 'employees' keys.
   ```

### Tips for Writing Good Queries

- Always request **JSON format** explicitly
- Specify the exact **key names** you want
- Use **comparative queries** for better visualizations
- Keep queries focused on 2-6 data points for clear charts

## Project Structure 📁

```
foundryAnalytics-chat/
├── azure_llm_analytics.py     # Core LLM client and visualization classes
├── streamlit_dashboard.py     # Interactive web dashboard
├── requirements.txt           # Python dependencies
├── config.example.py          # Configuration template
├── .gitignore                 # Git ignore patterns
├── README.md                  # This file
└── examples/
    └── sample_queries.py      # Example analytical queries
```

## Components 🔧

### 1. AzureLLMClient
Handles communication with Azure LLM endpoints using urllib.request with Bearer token authentication.

**Key Methods:**
- `query(prompt, temperature, max_tokens)`: Send queries to the LLM
- `test_connection()`: Verify endpoint connectivity

### 2. JSONExtractor
Intelligently extracts JSON data from LLM responses using multiple strategies.

**Key Methods:**
- `extract_json(text)`: Extract JSON from text using regex and parsing
- `extract_from_response(response)`: Extract from structured API responses

### 3. ChartGenerator
Creates interactive Plotly visualizations from extracted data.

**Key Methods:**
- `create_bar_chart(data, x_key, y_key, title)`: Generate bar charts
- `create_pie_chart(data, labels_key, values_key, title)`: Generate pie charts
- `auto_generate_chart(data, chart_type)`: Automatically determine best chart type

### 4. AnalyticsPipeline
Complete end-to-end pipeline combining querying, extraction, and visualization.

**Key Methods:**
- `run_query(prompt, temperature, max_tokens, chart_type)`: Execute full pipeline

## Configuration ⚙️

The application uses `config.py` for configuration (create from `config.example.py`):

```python
# Azure LLM Endpoint Configuration
AZURE_ENDPOINT_URL = "https://your-endpoint.azure.com/score"

# API Key for Authentication
API_KEY = "your-api-key-here"

# Default Parameters
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 800

# Chart Configuration
DEFAULT_CHART_TYPE = "auto"
```

**⚠️ Security Note**: Never commit `config.py` to version control. It's already in `.gitignore`.

## Dependencies 📦

- **streamlit** (≥1.28.0): Web dashboard framework
- **plotly** (≥5.17.0): Interactive visualizations
- **pandas** (≥2.0.0): Data manipulation
- **matplotlib** (≥3.7.0): Additional plotting support
- **seaborn** (≥0.12.0): Statistical visualizations

## Troubleshooting 🔍

### SSL Certificate Verification Errors

**Problem**: SSL certificate verification errors when connecting to Azure endpoint
**Solution**: 
- The application is currently using `azure_llm_analytics_dev` which has SSL verification disabled for development
- This is intended for development purposes only
- See [SSL_BYPASS_README.md](SSL_BYPASS_README.md) for detailed information
- For production, ensure your Azure endpoint has a valid SSL certificate and use `azure_llm_analytics` instead

### Connection Issues

**Problem**: "Connection failed" error
**Solution**: 
- Verify your API key is correct
- Check the endpoint URL is accessible
- Ensure you have internet connectivity
- Check for SSL certificate issues (see above)

### JSON Extraction Issues

**Problem**: "No structured data extracted"
**Solution**:
- Make sure your query explicitly requests JSON format
- Specify exact key names in your query
- Check the raw response tab to see what the LLM returned

### Chart Generation Issues

**Problem**: "Data was extracted but visualization failed"
**Solution**:
- Verify the extracted data has at least 2 columns
- Ensure one column is categorical and one is numeric
- Try different chart types (bar vs pie)

### Import Errors

**Problem**: Module not found errors
**Solution**:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Or install individually
pip install streamlit plotly pandas matplotlib seaborn
```

## Development 🛠️

### Running in Development Mode

```bash
# Install in development mode
pip install -e .

# Run with auto-reload
streamlit run streamlit_dashboard.py --server.runOnSave true
```

### Adding New Features

1. **New Chart Types**: Extend `ChartGenerator` class
2. **Custom Extractors**: Modify `JSONExtractor` strategies
3. **Additional Examples**: Add to `SAMPLE_QUERIES` in `examples/sample_queries.py`

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is open source and available under the MIT License.

## Support 💬

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the example queries for guidance

## Acknowledgments 🙏

Built with:
- [Streamlit](https://streamlit.io/) - Web framework
- [Plotly](https://plotly.com/) - Visualization library
- [Pandas](https://pandas.pydata.org/) - Data manipulation

---

**Happy Analyzing! 📊✨**