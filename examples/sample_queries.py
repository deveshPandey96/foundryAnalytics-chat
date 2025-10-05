"""
Sample Queries for Azure LLM Analytics

This module contains example queries that demonstrate how to use
the Azure LLM Analytics system for comparative analysis.
"""

from azure_llm_analytics import AzureLLMClient, AnalyticsPipeline


# Example queries that return JSON data for visualization
SAMPLE_QUERIES = [
    {
        "title": "Phase Comparison - J&K Bank",
        "query": "Compare the number of tasks in phase 3 and phase 6 of J&K Bank. Return the result in JSON format with 'phase' and 'tasks' keys.",
        "description": "Compares task counts across different phases",
        "expected_keys": ["phase", "tasks"]
    },
    {
        "title": "Use Cases Comparison - Banks",
        "query": "Compare number of use cases of CSB bank and J&K Bank. Return the result in JSON format with 'customer' and 'use cases' keys.",
        "description": "Compares use cases between two banks",
        "expected_keys": ["customer", "use cases"]
    },
    {
        "title": "Quarterly Revenue",
        "query": "Show the quarterly revenue for Q1, Q2, Q3, and Q4. Return as JSON with 'quarter' and 'revenue' keys.",
        "description": "Displays revenue across quarters",
        "expected_keys": ["quarter", "revenue"]
    },
    {
        "title": "Department Headcount",
        "query": "Compare the number of employees in Engineering, Sales, and Marketing departments. Return as JSON with 'department' and 'employees' keys.",
        "description": "Compares employee counts across departments",
        "expected_keys": ["department", "employees"]
    },
    {
        "title": "Product Sales Comparison",
        "query": "Compare sales of Product A, Product B, and Product C. Return as JSON with 'product' and 'sales' keys.",
        "description": "Compares sales figures for different products",
        "expected_keys": ["product", "sales"]
    },
    {
        "title": "Regional Performance",
        "query": "Compare performance scores for North, South, East, and West regions. Return as JSON with 'region' and 'score' keys.",
        "description": "Compares performance across regions",
        "expected_keys": ["region", "score"]
    }
]


def run_example(
    client: AzureLLMClient,
    example_index: int = 0,
    temperature: float = 0.7,
    max_tokens: int = 800,
    chart_type: str = "auto"
):
    """
    Run a sample query and display results.
    
    Args:
        client: AzureLLMClient instance
        example_index: Index of the example to run (0-based)
        temperature: Sampling temperature
        max_tokens: Maximum tokens
        chart_type: Type of chart to generate
        
    Returns:
        Result dictionary from the analytics pipeline
    """
    if example_index < 0 or example_index >= len(SAMPLE_QUERIES):
        raise ValueError(f"Example index must be between 0 and {len(SAMPLE_QUERIES) - 1}")
    
    example = SAMPLE_QUERIES[example_index]
    pipeline = AnalyticsPipeline(client)
    
    print(f"\n{'='*60}")
    print(f"Running Example: {example['title']}")
    print(f"{'='*60}")
    print(f"Description: {example['description']}")
    print(f"Query: {example['query']}")
    print(f"Expected Keys: {example['expected_keys']}")
    print(f"{'='*60}\n")
    
    result = pipeline.run_query(
        example['query'],
        temperature=temperature,
        max_tokens=max_tokens,
        chart_type=chart_type
    )
    
    if result['success']:
        print("✅ Query successful!")
        
        if result.get('extracted_data'):
            print(f"\n📊 Extracted Data:")
            import json
            print(json.dumps(result['extracted_data'], indent=2))
            
            if result.get('chart'):
                print("\n📈 Chart generated successfully!")
            else:
                print("\n⚠️ Could not generate chart from data")
        else:
            print("\n⚠️ No structured data extracted from response")
    else:
        print(f"❌ Query failed: {result.get('error')}")
    
    return result


def list_examples():
    """List all available example queries."""
    print("\n📚 Available Example Queries:")
    print("=" * 60)
    
    for i, example in enumerate(SAMPLE_QUERIES):
        print(f"\n{i}. {example['title']}")
        print(f"   {example['description']}")
        print(f"   Expected keys: {', '.join(example['expected_keys'])}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    import sys
    
    # Check if config exists
    try:
        from config import AZURE_ENDPOINT_URL, API_KEY
    except ImportError:
        print("❌ Error: config.py not found!")
        print("Please copy config.example.py to config.py and update with your credentials.")
        sys.exit(1)
    
    # Create client
    client = AzureLLMClient(AZURE_ENDPOINT_URL, API_KEY)
    
    # Test connection
    print("Testing connection...")
    success, message = client.test_connection()
    print(message)
    
    if not success:
        sys.exit(1)
    
    # List examples
    list_examples()
    
    # Run first example if no arguments provided
    if len(sys.argv) < 2:
        print("\n💡 Running first example (use: python sample_queries.py <example_number>)")
        run_example(client, 0)
    else:
        try:
            example_num = int(sys.argv[1])
            run_example(client, example_num)
        except ValueError:
            print("❌ Please provide a valid example number")
            list_examples()
        except Exception as e:
            print(f"❌ Error: {str(e)}")
