"""
Streamlit Dashboard for Azure LLM Analytics

Interactive web interface for querying Azure LLM and visualizing responses.
"""

import streamlit as st
from azure_llm_analytics_dev import AzureLLMClient, AnalyticsPipeline
import json

# Load configuration from config file
try:
    from config import AZURE_ENDPOINT_URL, API_KEY, DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS
except ImportError:
    st.error("⚠️ Configuration file not found! Please create config.py from config.example.py")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Azure LLM Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Azure LLM Analytics Dashboard")
st.markdown("""
Professional analytics dashboard for querying Azure LLM and visualizing responses.
""")

# Sidebar for tips
st.sidebar.markdown("### 💡 Tips")
st.sidebar.markdown("""
- Always request JSON format in your queries
- Specify the exact keys you want in the response
- Use comparative queries for better visualizations
- Try different graph types to visualize your data
""")

# Main content area - Chat Interface
st.subheader("💬 Query Input")

# Get query from session state if available
default_query = st.session_state.get('selected_query', '')

query = st.text_area(
    "Enter your query:",
    value=default_query,
    height=120,
    placeholder="Example: Compare the number of tasks in phase 3 and phase 6 of J&K Bank. Return the result in JSON format with 'phase' and 'tasks' keys.",
    help="Enter a query that requests data in JSON format for best results"
)

# Clear the selected query after use
if 'selected_query' in st.session_state:
    del st.session_state.selected_query

col_btn1, col_btn2 = st.columns([1, 5])

with col_btn1:
    submit_button = st.button("🚀 Submit", type="primary", use_container_width=True)

with col_btn2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

# Example queries section
with st.expander("📝 Example Queries"):
    example_queries = [
        "Compare the number of tasks in phase 3 and phase 6 of J&K Bank. Return the result in JSON format with 'phase' and 'tasks' keys.",
        "Compare number of use cases of CSB bank and J&K Bank. Return the result in JSON format with 'customer' and 'use cases' keys.",
        "Show the quarterly revenue for Q1, Q2, Q3, and Q4. Return as JSON with 'quarter' and 'revenue' keys.",
        "Compare the number of employees in Engineering, Sales, and Marketing departments. Return as JSON with 'department' and 'employees' keys.",
    ]
    
    cols = st.columns(2)
    for i, example in enumerate(example_queries):
        with cols[i % 2]:
            if st.button(f"Example {i+1}", key=f"example_{i}", use_container_width=True):
                st.session_state.selected_query = example
                st.rerun()

# Handle clear button
if clear_button:
    st.rerun()

# Handle submit button
if submit_button:
    if not query:
        st.error("⚠️ Please enter a query!")
    else:
        # Create client and pipeline using config values
        client = AzureLLMClient(AZURE_ENDPOINT_URL, API_KEY)
        pipeline = AnalyticsPipeline(client)
        
        # Store initial chart type in session state
        if 'chart_type' not in st.session_state:
            st.session_state.chart_type = "bar"
        
        # Run query with config values (initial chart type doesn't matter, we'll regenerate)
        with st.spinner("🔄 Processing your query..."):
            result = pipeline.run_query(
                query,
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=DEFAULT_MAX_TOKENS,
                chart_type=st.session_state.chart_type
            )
        
        # Store result in session state for chart type switching
        st.session_state.result = result
        st.session_state.query_submitted = True

# Display results if available
if st.session_state.get('query_submitted', False) and 'result' in st.session_state:
    result = st.session_state.result
    
    if not result['success']:
        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
    else:
        st.success("✅ Query completed successfully!")
        
        # Separator
        st.markdown("---")
        
        # Create tabs for Text Output and Graph Output
        tab1, tab2 = st.tabs(["📝 Text Output", "📊 Graph Output"])
        
        with tab1:
            st.subheader("Response")
            
            # Show raw response text
            if result.get('response'):
                response_data = result['response'].get('response', {})
                
                # Display as formatted JSON if available
                if response_data:
                    st.json(response_data)
                
                # Show raw text if available
                if result['response'].get('raw_text'):
                    with st.expander("📄 View as plain text"):
                        st.text(result['response']['raw_text'])
            
            # Show extracted data
            if result.get('extracted_data'):
                st.markdown("---")
                st.subheader("Extracted Data")
                
                # Display as table
                import pandas as pd
                df = pd.DataFrame(result['extracted_data'])
                st.dataframe(df, use_container_width=True)
                
                # Display as JSON
                st.markdown("**JSON Format:**")
                st.json(result['extracted_data'])
                
                # Download button
                json_str = json.dumps(result['extracted_data'], indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name="extracted_data.json",
                    mime="application/json"
                )
            else:
                st.info("ℹ️ No structured data was extracted from the response.")
        
        with tab2:
            st.subheader("Visualization")
            
            if result.get('extracted_data'):
                # Chart type selector in the Graph Output tab
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    selected_chart_type = st.selectbox(
                        "Select Graph Type",
                        options=["bar", "pie", "line", "scatter"],
                        index=["bar", "pie", "line", "scatter"].index(st.session_state.get('chart_type', 'bar')),
                        key="chart_type_selector"
                    )
                
                # Regenerate chart if type changed
                if selected_chart_type != st.session_state.get('chart_type', 'bar'):
                    st.session_state.chart_type = selected_chart_type
                    # Recreate chart with new type
                    client = AzureLLMClient(AZURE_ENDPOINT_URL, API_KEY)
                    pipeline = AnalyticsPipeline(client)
                    try:
                        new_chart = pipeline.create_chart(result['extracted_data'], selected_chart_type)
                        result['chart'] = new_chart
                        st.session_state.result = result
                    except Exception as e:
                        st.error(f"Error creating chart: {str(e)}")
                
                # Display chart
                if result.get('chart'):
                    st.plotly_chart(result['chart'], use_container_width=True)
                else:
                    st.warning("⚠️ Unable to generate visualization. Please check your data format.")
            else:
                st.info("ℹ️ No structured data found in the response. The LLM may not have returned JSON format.")
                st.markdown("**Tip:** Try rephrasing your query to explicitly request JSON format.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Azure LLM Analytics Dashboard | Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
