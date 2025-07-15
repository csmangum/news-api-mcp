#!/usr/bin/env python3
"""
Direct test of the MCP server functionality
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

# Add the src directory to path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Import our MCP server components directly
from news_api_mcp.tools import make_news_api_request, format_articles, API_KEY
import httpx

async def test_news_api_directly():
    """Test the News API functionality directly"""
    
    print("🚀 Testing News API MCP Server Components")
    print("=" * 60)
    
    # Check API key
    if not API_KEY:
        print("❌ ERROR: NEWS_API_KEY not found in environment")
        print("Make sure your .env file contains: NEWS_API_KEY=your_actual_key")
        return
    
    print(f"✅ API Key loaded: {API_KEY[:10]}..." if len(API_KEY) > 10 else f"✅ API Key loaded: {API_KEY}")
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Search for news
        print("\n📰 Test 1: Searching for AI news...")
        print("-" * 40)
        
        search_params = {
            "q": "artificial intelligence",
            "pageSize": 3,
            "language": "en",
            "sortBy": "publishedAt"
        }
        
        result = await make_news_api_request(client, "everything", search_params)
        
        if isinstance(result, str):
            print(f"❌ Error: {result}")
        else:
            articles = result.get("articles", [])
            total = result.get("totalResults", 0)
            print(f"✅ Found {total} articles, showing first {len(articles)}:")
            print(format_articles(articles, limit=2))
        
        # Test 2: Get top headlines
        print("\n📈 Test 2: Getting US tech headlines...")
        print("-" * 40)
        
        headlines_params = {
            "country": "us",
            "category": "technology",
            "pageSize": 2
        }
        
        result = await make_news_api_request(client, "top-headlines", headlines_params)
        
        if isinstance(result, str):
            print(f"❌ Error: {result}")
        else:
            articles = result.get("articles", [])
            total = result.get("totalResults", 0)
            print(f"✅ Found {total} headlines, showing first {len(articles)}:")
            print(format_articles(articles, limit=2))
        
        # Test 3: Get news sources
        print("\n🌐 Test 3: Getting tech news sources...")
        print("-" * 40)
        
        sources_params = {
            "category": "technology",
            "language": "en"
        }
        
        result = await make_news_api_request(client, "top-headlines/sources", sources_params)
        
        if isinstance(result, str):
            print(f"❌ Error: {result}")
        else:
            sources = result.get("sources", [])
            print(f"✅ Found {len(sources)} tech sources:")
            for i, source in enumerate(sources[:3], 1):
                print(f"  {i}. {source.get('name')} ({source.get('id')})")
    
    print("\n🎉 Testing complete!")

if __name__ == "__main__":
    asyncio.run(test_news_api_directly()) 