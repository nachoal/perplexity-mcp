# server.py
from mcp.server.fastmcp import FastMCP
import sys
import os
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create an MCP server
mcp = FastMCP("Perplexity Web Search")

# Initialize OpenAI client with Perplexity base URL
def get_perplexity_client():
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        raise ValueError("PERPLEXITY_API_KEY environment variable is not set")
    return OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

@mcp.tool()
def search_web(query: str, recency: Optional[str] = "month") -> str:
    """
    Search the web using Perplexity API and return results.
    
    Args:
        query: The search query string
        recency: Filter results by time period - 'day', 'week', 'month' (default), or 'year'
    
    Returns:
        Search results as text
    """
    # Validate recency parameter
    valid_recency = ["day", "week", "month", "year"]
    if recency not in valid_recency:
        recency = "month"  # Default to month if invalid
    
    # Create system message with recency filter
    system_message = f"""You are a web search assistant. Search the web for information about the query. 
Only include results from the past {recency}. 
Provide a comprehensive answer with the following:
1. A detailed summary of the search results
2. Key facts and information found
3. Include sources with URLs for verification
4. Mention any conflicting information if present"""
    
    try:
        # Initialize Perplexity client
        client = get_perplexity_client()
        
        # Make API call to Perplexity
        response = client.chat.completions.create(
            model="sonar-pro",  # Using Perplexity's supported model
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": query}
            ]
        )
        
        # Return the raw text response
        return response.choices[0].message.content
    
    except Exception as e:
        # Return error information as text
        return f"Error searching the web: {str(e)}"

@mcp.prompt()
def web_search_prompt(query: str, recency: Optional[str] = "month") -> str:
    """
    Create a prompt for searching the web with Perplexity.
    
    Args:
        query: The search query
        recency: Time period filter - 'day', 'week', 'month' (default), or 'year'
    """
    # Validate recency parameter
    valid_recency = ["day", "week", "month", "year"]
    if recency not in valid_recency:
        recency = "month"  # Default to month if invalid
    
    time_period_text = {
        "day": "the past 24 hours",
        "week": "the past week",
        "month": "the past month",
        "year": "the past year"
    }
    
    return f"""
I need you to search the web for information about: {query}

Please focus on results from {time_period_text[recency]}.

After searching, please:
1. Summarize the key findings
2. Highlight any important facts or data points
3. Mention any conflicting information if present
4. Cite your sources with links

This information will help me understand the current state of this topic.
"""

# Run the server when this script is executed directly
if __name__ == "__main__":
    try:
        print("Starting Perplexity Web Search MCP server...", file=sys.stderr)
        mcp.run()
    except Exception as e:
        print(f"Error running MCP server: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
