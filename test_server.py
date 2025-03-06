#!/usr/bin/env python3
# test_server.py
import os
import argparse
from dotenv import load_dotenv
from server import search_web

# Load environment variables from .env file
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Test the Perplexity Web Search MCP server")
    parser.add_argument("query", help="The search query")
    parser.add_argument("--recency", choices=["day", "week", "month", "year"], 
                        default="month", help="Filter results by time period")
    args = parser.parse_args()
    
    # Check if PERPLEXITY_API_KEY is set
    if not os.environ.get("PERPLEXITY_API_KEY"):
        print("Error: PERPLEXITY_API_KEY environment variable is not set")
        print("Please set it with: export PERPLEXITY_API_KEY='your-api-key-here'")
        print("Or create a .env file with PERPLEXITY_API_KEY=your-api-key-here")
        return 1
    
    print(f"Searching for: {args.query}")
    print(f"Time period: {args.recency}")
    print("Fetching results...")
    
    try:
        # Call the search_web function
        results = search_web(args.query, args.recency)
        
        # Print the results
        print("\nResults:")
        print(results)
        
        return 0
    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 