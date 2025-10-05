"""
Streamlit Dashboard for Azure LLM Analytics

Interactive web interface for querying Azure LLM and visualizing responses.
"""

import streamlit as st
from azure_llm_analytics import AzureLLMClient, AnalyticsPipeline
import json


# Page configuration
st.set_page_config(
    page_title="Azure LLM Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Azure LLM Analytics Dashboard")
st.markdown("""
This dashboard allows you to query Azure LLM endpoints and automatically visualize JSON responses.
Perfect for comparative analysis and data exploration.
""")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")

# Endpoint URL
endpoint_url = st.sidebar.text_input(
    "Azure Endpoint URL",
    value="https://endpointNew-29sep-bdtrm.eastus2.inference.ml.azure.com/score",
    help="Enter your Azure LLM endpoint URL"
)

# API Key
api_key = st.sidebar.text_input(
    "API Key",
    type="password",
    help="Enter your API key for authentication"
)

# Test connection button
if st.sidebar.button("🔌 Test Connection"):
    if not api_key:
        st.sidebar.error("Please enter an API key first!")
    else:
        with st.sidebar.spinner("Testing connection..."):
            client = AzureLLMClient(endpoint_url, api_key)
            success, message = client.test_connection()
            if success:
                st.sidebar.success(message)
            else:
                st.sidebar.error(message)

st.sidebar.markdown("---")

# Parameters
st.sidebar.header("🎛️ Parameters")
temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Controls randomness in responses. Higher values = more creative"
)

max_tokens = st.sidebar.slider(
    "Max Tokens",
    min_value=100,
    max_value=2000,
    value=800,
    step=100,
    help="Maximum length of the response"
)

chart_type = st.sidebar.selectbox(
    "Chart Type",
    options=["auto", "bar", "pie"],
    help="Type of chart to generate from data"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 💡 Tips")
st.sidebar.markdown("""
- Always request JSON format in your queries
- Specify the exact keys you want in the response
- Use comparative queries for better visualizations
""")

# Main content area
col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("📝 Example Queries")
    
    example_queries = [
        "Compare the number of tasks in phase 3 and phase 6 of J&K Bank. Return the result in JSON format with 'phase' and 'tasks' keys.",
        "Compare number of use cases of CSB bank and J&K Bank. Return the result in JSON format with 'customer' and 'use cases' keys.",
        "Show the quarterly revenue for Q1, Q2, Q3, and Q4. Return as JSON with 'quarter' and 'revenue' keys.",
        "Compare the number of employees in Engineering, Sales, and Marketing departments. Return as JSON with 'department' and 'employees' keys.",
    ]
    
    for i, example in enumerate(example_queries, 1):
        if st.button(f"Example {i}", key=f"example_{i}", use_container_width=True):
            st.session_state.selected_query = example
    
    st.markdown("---")
    st.markdown("**Click an example to load it into the query box**")

with col1:
    st.subheader("🔍 Query Input")
    
    # Get query from session state if available
    default_query = st.session_state.get('selected_query', '')
    
    query = st.text_area(
        "Enter your query:",
        value=default_query,
        height=150,
        placeholder="Example: Compare the number of tasks in phase 3 and phase 6 of J&K Bank. Return the result in JSON format with 'phase' and 'tasks' keys.",
        help="Enter a query that requests data in JSON format for best results"
    )
    
    # Clear the selected query after use
    if 'selected_query' in st.session_state:
        del st.session_state.selected_query
    
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])
    
    with col_btn1:
        submit_button = st.button("🚀 Submit Query", type="primary", use_container_width=True)
    
    with col_btn2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)

# Handle clear button
if clear_button:
    st.rerun()

# Handle submit button
if submit_button:
    if not api_key:
        st.error("⚠️ Please enter an API key in the sidebar!")
    elif not query:
        st.error("⚠️ Please enter a query!")
    else:
        # Create client and pipeline
        client = AzureLLMClient(endpoint_url, api_key)
        pipeline = AnalyticsPipeline(client)
        
        # Run query
        with st.spinner("🔄 Processing your query..."):
            result = pipeline.run_query(
                query,
                temperature=temperature,
                max_tokens=max_tokens,
                chart_type=chart_type
            )
        
        if not result['success']:
            st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        else:
            st.success("✅ Query completed successfully!")
            
            # Create tabs for different views
            tab1, tab2, tab3 = st.tabs(["📊 Visualization", "📋 Data", "🔍 Raw Response"])
            
            with tab1:
                st.subheader("Visualization")
                
                if result.get('chart'):
                    st.plotly_chart(result['chart'], use_container_width=True)
                elif result.get('extracted_data'):
                    st.warning("⚠️ Data was extracted but visualization failed. Check the Data tab.")
                else:
                    st.info("ℹ️ No structured data found in the response. The LLM may not have returned JSON format.")
                    st.markdown("**Tip:** Try rephrasing your query to explicitly request JSON format.")
            
            with tab2:
                st.subheader("Extracted Data")
                
                if result.get('extracted_data'):
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
            
            with tab3:
                st.subheader("Raw Response")
                
                response_data = result['response'].get('response', {})
                st.json(response_data)
                
                # Show raw text if available
                if result['response'].get('raw_text'):
                    with st.expander("📄 View as text"):
                        st.text(result['response']['raw_text'])

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Azure LLM Analytics Dashboard | Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
