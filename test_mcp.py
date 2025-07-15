#!/usr/bin/env python3
"""
Simple test script to interact with the running MCP server
"""

import json
import sys
import subprocess
import asyncio

async def test_mcp_server():
    """Test the MCP server by sending sample requests"""
    
    # Test 1: List available tools
    print("🔧 Testing: List Tools")
    list_tools_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }
    
    print(f"Request: {json.dumps(list_tools_request, indent=2)}")
    print("-" * 50)
    
    # Test 2: Search for news
    print("\n📰 Testing: Search News")
    search_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "search-news",
            "arguments": {
                "query": "artificial intelligence",
                "page_size": 3
            }
        }
    }
    
    print(f"Request: {json.dumps(search_request, indent=2)}")
    print("-" * 50)
    
    # Test 3: Get top headlines
    print("\n📈 Testing: Top Headlines")
    headlines_request = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "get-top-headlines",
            "arguments": {
                "country": "us",
                "category": "technology",
                "page_size": 2
            }
        }
    }
    
    print(f"Request: {json.dumps(headlines_request, indent=2)}")
    print("-" * 50)

if __name__ == "__main__":
    print("🚀 MCP Server Test Suite")
    print("=" * 50)
    asyncio.run(test_mcp_server())
    print("\n✅ Test requests prepared!")
    print("💡 To actually test, you'll need to send these JSON-RPC requests to your running server") 