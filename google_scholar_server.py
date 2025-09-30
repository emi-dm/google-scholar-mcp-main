from typing import Any, List, Dict, Optional
import asyncio
import logging
from fastmcp import FastMCP
from google_scholar_web_search import google_scholar_search, advanced_google_scholar_search
from scholarly import scholarly
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize FastMCP server for PubMed and Google Scholar
mcp = FastMCP("Google Scholar Search MCP 📚")

@mcp.prompt("Search Google Scholar for articles")
async def search_google_scholar_articles(topic: str) -> str:
    """Prompt to search for articles on Google Scholar based on a given topic.
    Args:
        topic: The topic to search for articles.
    Returns:
        A prompt string to guide the user in searching for articles."""
    
    logging.info(f"Giving prompt. Searching Google Scholar for articles on topic: {topic}")
    return f"Search for recent and relevant academic articles on the topic: '{topic}' using Google Scholar. Provide a list of articles with their titles, authors, publication year, and a brief summary if available. Use `google_scholar_search` tool."

@mcp.tool()
async def search_google_scholar_key_words(query: str, num_results: int = 5000) -> List[Dict[str, Any]]:
    logging.info(f"Searching Google Scholar for articles with query: {query}, num_results: {num_results}")
    """
    Search for articles on Google Scholar using key words.

    Args:
        query: Search query string
        num_results: Number of results to return (default: 5)

    Returns:
        List of dictionaries containing article information
    """
    try:
        results = await asyncio.to_thread(google_scholar_search, query, num_results)
        return results
    except Exception as e:
        return [{"error": f"An error occurred while searching Google Scholar: {str(e)}"}]

@mcp.tool()
async def search_google_scholar(query: str, author: Optional[str] = None, year_range: Optional[tuple] = None, num_results: int = 5000) -> List[Dict[str, Any]]:
    """
    Search for articles on Google Scholar.

    Args:
        query: General search query
        author: Author name
        year_range: tuple containing (start_year, end_year)
        num_results: Number of results to return (default: 5)

    Returns:
        List of dictionaries containing article information
    """
    logging.info(f"Performing advanced search with parameters: {locals()}")
    try:
        results = await asyncio.to_thread(
            advanced_google_scholar_search,
            query, author, year_range, num_results
        )
        return results
    except Exception as e:
        return [{"error": f"An error occurred while performing advanced search on Google Scholar: {str(e)}"}]

@mcp.tool()
async def get_author_info(author_name: str) -> Dict[str, Any]:
    logging.info(f"Retrieving author information for: {author_name}")
    """
    Get detailed information about an author from Google Scholar.

    Args:
        author_name: Name of the author to search for

    Returns:
        Dictionary containing author information
    """
    try:
        search_query = scholarly.search_author(author_name)
        author = await asyncio.to_thread(next, search_query)
        filled_author = await asyncio.to_thread(scholarly.fill, author)
        
        # Extract relevant information
        author_info = {
            "name": filled_author.get("name", "N/A"),
            "affiliation": filled_author.get("affiliation", "N/A"),
            "interests": filled_author.get("interests", []),
            "citedby": filled_author.get("citedby", 0),
            "publications": [
                {
                    "title": pub.get("bib", {}).get("title", "N/A"),
                    "year": pub.get("bib", {}).get("pub_year", "N/A"),
                    "citations": pub.get("num_citations", 0)
                }
                for pub in filled_author.get("publications", [])[:5]  # Limit to top 5 publications
            ]
        }
        return author_info
    except Exception as e:
        return {"error": f"An error occurred while retrieving author information: {str(e)}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Scholar MCP Server")
    parser.add_argument("--mode", type=str, choices=["streamable-http", "stdio"], default="streamable-http", help="Transport mode for the MCP server")
    args = parser.parse_args()
    if args.mode == "stdio":
        mcp.run(transport=args.mode)
    else:
        mcp.run(transport=args.mode , host="0.0.0.0", port=3000)
