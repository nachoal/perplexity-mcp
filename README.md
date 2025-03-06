# Perplexity Web Search MCP Server

A simple MCP (Model Context Protocol) server that provides web search functionality using the Perplexity API. This server allows Claude or other MCP-compatible AI assistants to search the web and get up-to-date information.

## Features

- Search the web with Perplexity's powerful search capabilities
- Get comprehensive search results with sources and citations
- Filter results by time period (day, week, month, year)
- Includes a ready-to-use prompt template for web searches
- Supports loading API key from environment variables or .env file

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -e .
   ```
   or
   ```
   uv pip install -e .
   ```

## Configuration

You can set the `PERPLEXITY_API_KEY` environment variable with your Perplexity API key:

```bash
export PERPLEXITY_API_KEY="your-api-key-here"
```

Alternatively, you can create a `.env` file in the project root with the following content:

```
PERPLEXITY_API_KEY=your-api-key-here
```

A sample `.env.example` file is provided for reference.

To get a Perplexity API key:
1. Visit [Perplexity API Settings](https://www.perplexity.ai/settings/api)
2. Create an account if you don't have one
3. Generate an API key

## Usage

### Running the server

```bash
python server.py
```

### Testing the server

You can test the server functionality without running the full MCP server using the included test script:

```bash
python test_server.py "your search query here" --recency month
```

Options for `--recency` are: day, week, month (default), year

### Using with Claude Desktop

1. Edit your Claude Desktop configuration file:
   - On macOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
   - On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

2. Add the following configuration:
   ```json
   {
     "perplexity-mcp": {
       "env": {
         "PERPLEXITY_API_KEY": "your-api-key-here"
       },
       "command": "python",
       "args": [
         "/path/to/server.py"
       ]
     }
   }
   ```

3. Restart Claude Desktop

### Example Prompts for Claude

- "Search the web for the latest news about artificial intelligence"
- "Use Perplexity to find information about climate change published in the past week"
- "Search for recent research papers on quantum computing from the past month"

## API Reference

### Tool: `search_web(query: str, recency: str = "month") -> str`

Search the web using Perplexity API and return results.

**Parameters:**
- `query`: The search query string
- `recency`: Filter results by time period - 'day', 'week', 'month' (default), or 'year'

**Returns:**
A comprehensive text response containing:
1. A detailed summary of the search results
2. Key facts and information found
3. Sources with URLs for verification
4. Any conflicting information if present

### Prompt: `web_search_prompt(query: str, recency: str = "month") -> str`

Creates a prompt template for searching the web with Perplexity.

**Parameters:**
- `query`: The search query
- `recency`: Time period filter - 'day', 'week', 'month' (default), or 'year'

**Returns:**
A formatted prompt string that instructs the AI to:
1. Search for the specified query
2. Focus on results from the specified time period
3. Summarize key findings
4. Highlight important facts
5. Mention conflicting information
6. Cite sources with links

## License

MIT
