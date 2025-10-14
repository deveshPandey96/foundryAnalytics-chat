"""
Streamlit Dashboard for Azure LLM Analytics

Interactive web interface for querying Azure LLM and visualizing responses.
"""

import streamlit as st
from azure_llm_analytics_dev import AzureLLMClient, AnalyticsPipeline
import json
import re

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

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Custom CSS for chat-like interface
st.markdown("""
<style>
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* Main container */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Input box styling */
    .stTextInput > div > div > input {
        border-radius: 1.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 1.5rem;
    }
    
    /* Make the conversation section scrollable */
    .conversation-container {
        max-height: 600px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

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

# Display chat history first
if st.session_state.chat_history:
    st.markdown("### 💬 Conversation")
    for i, chat in enumerate(st.session_state.chat_history):
        # User message
        with st.chat_message("user"):
            st.markdown(chat['query'])
        
        # Assistant message
        with st.chat_message("assistant"):
            # Display text response
            if chat.get('text_response'):
                st.markdown(chat['text_response'])
            
            # Display tabs for detailed view
            if chat.get('has_data'):
                tab1, tab2 = st.tabs(["📝 Detailed Response", "📊 Graph View"])
                
                with tab1:
                    # Show extracted data
                    if chat.get('extracted_data'):
                        st.markdown("**Extracted Data:**")
                        import pandas as pd
                        df = pd.DataFrame(chat['extracted_data'])
                        st.dataframe(df, use_container_width=True)
                        
                        # Download button
                        json_str = json.dumps(chat['extracted_data'], indent=2)
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_str,
                            file_name=f"data_{i}.json",
                            mime="application/json",
                            key=f"download_{i}"
                        )
                
                with tab2:
                    if chat.get('chart'):
                        # Chart type selector
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            selected_chart_type = st.selectbox(
                                "Select Graph Type",
                                options=["bar", "pie", "line", "scatter"],
                                index=["bar", "pie", "line", "scatter"].index(chat.get('chart_type', 'bar')),
                                key=f"chart_type_{i}"
                            )
                        
                        # Regenerate chart if type changed
                        if selected_chart_type != chat.get('chart_type', 'bar'):
                            client = AzureLLMClient(AZURE_ENDPOINT_URL, API_KEY)
                            pipeline = AnalyticsPipeline(client)
                            try:
                                new_chart = pipeline.create_chart(chat['extracted_data'], selected_chart_type)
                                st.session_state.chat_history[i]['chart'] = new_chart
                                st.session_state.chat_history[i]['chart_type'] = selected_chart_type
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error creating chart: {str(e)}")
                        
                        st.plotly_chart(chat['chart'], use_container_width=True)
                    else:
                        st.info("ℹ️ No visualization available for this response.")

    st.markdown("---")

# Main content area - Chat Interface
st.subheader("💬 Ask a Question")

# Get query from session state if available
default_query = st.session_state.get('selected_query', '')

query = st.text_input(
    "Enter your query:",
    value=default_query,
    placeholder="Example: Compare the number of tasks in phase 3 and phase 6 of J&K Bank...",
    help="Enter a query that requests data in JSON format for best results",
    key="query_input"
)

# Clear the selected query after use
if 'selected_query' in st.session_state:
    del st.session_state.selected_query

col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 4])

with col_btn1:
    submit_button = st.button("🚀 Submit", type="primary", use_container_width=True)

with col_btn2:
    clear_chat_button = st.button("🗑️ Clear Chat", use_container_width=True)

with col_btn3:
    st.write("")  # Empty space

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

# Handle clear chat button
if clear_chat_button:
    st.session_state.chat_history = []
    if 'query_submitted' in st.session_state:
        del st.session_state.query_submitted
    if 'result' in st.session_state:
        del st.session_state.result
    st.rerun()

# Helper function to extract readable text from LLM response
def extract_readable_text(result):
    """Extract human-readable text from LLM response, converting JSON to narrative format."""
    raw_text = result.get('response', {}).get('raw_text', '')
    
    # If we have extracted data, create a narrative summary
    if result.get('extracted_data'):
        data = result['extracted_data']
        
        # Try to create a natural language summary
        try:
            import pandas as pd
            df = pd.DataFrame(data)
            
            # Get column names
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if text_cols and numeric_cols:
                x_col = text_cols[0]
                y_col = numeric_cols[0]
                
                # Build a summary
                summary = f"Here's the data for {y_col} across different {x_col}:\n\n"
                for _, row in df.iterrows():
                    summary += f"• **{row[x_col]}**: {row[y_col]}\n"
                
                # Add total if numeric
                if len(df) > 1:
                    total = df[y_col].sum()
                    summary += f"\n**Total {y_col}**: {total}"
                
                return summary
        except:
            pass
    
    # If no extracted data or failed to create summary, clean up the raw text
    # Remove JSON blocks and formatting
    text = re.sub(r'```json\s*', '', raw_text)
    text = re.sub(r'```\s*', '', text)
    
    # Try to extract just the explanatory text (non-JSON part)
    lines = text.split('\n')
    readable_lines = []
    in_json = False
    
    for line in lines:
        stripped = line.strip()
        # Skip JSON array/object markers
        if stripped.startswith('[') or stripped.startswith('{'):
            in_json = True
        if stripped.endswith(']') or stripped.endswith('}'):
            in_json = False
            continue
        
        if not in_json and stripped and not stripped.startswith('"'):
            # This looks like explanatory text
            readable_lines.append(line)
    
    if readable_lines:
        return '\n'.join(readable_lines)
    
    # Fallback: return raw text
    return raw_text

# Handle submit button
if submit_button:
    if not query:
        st.error("⚠️ Please enter a query!")
    else:
        # Create client and pipeline using config values
        client = AzureLLMClient(AZURE_ENDPOINT_URL, API_KEY)
        pipeline = AnalyticsPipeline(client)
        
        # Run query with config values
        with st.spinner("🔄 Processing your query..."):
            result = pipeline.run_query(
                query,
                temperature=DEFAULT_TEMPERATURE,
                max_tokens=DEFAULT_MAX_TOKENS,
                chart_type="bar"  # Default chart type
            )
        
        if not result['success']:
            st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
        else:
            # Extract readable text from response
            text_response = extract_readable_text(result)
            
            # Create chat entry
            chat_entry = {
                'query': query,
                'text_response': text_response,
                'extracted_data': result.get('extracted_data'),
                'chart': result.get('chart'),
                'chart_type': 'bar',
                'has_data': result.get('extracted_data') is not None,
                'raw_response': result.get('response', {}).get('raw_text', '')
            }
            
            # Add to chat history
            st.session_state.chat_history.append(chat_entry)
            
            # Clear the input
            st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Azure LLM Analytics Dashboard | Built with Streamlit & Plotly</p>
</div>
""", unsafe_allow_html=True)
