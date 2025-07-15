#!/usr/bin/env python3
"""
Simple local test of MCP server - sends one request and shows response
"""

import json
import subprocess
import sys
import os
import time

def test_single_request():
    """Send a single request to the MCP server and show the response"""
    
    print("🔍 Testing MCP Server with Single Request")
    print("=" * 50)
    
    cmd = [sys.executable, "-m", "src.news_api_mcp"]
    
    try:
        # Start MCP server
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        
        # Initialize the connection
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "local-test", "version": "1.0.0"}
            }
        }
        
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read init response
        init_response = process.stdout.readline()
        print("📡 Initialization successful!")
        
        # Send a tools/list request
        list_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        process.stdin.write(json.dumps(list_request) + "\n")
        process.stdin.flush()
        
        # Read tools list response
        tools_response = process.stdout.readline()
        tools_data = json.loads(tools_response.strip())
        tools = tools_data.get('result', {}).get('tools', [])
        
        print(f"\n🔧 Available Tools ({len(tools)}):")
        for i, tool in enumerate(tools, 1):
            print(f"  {i}. {tool['name']}")
            print(f"     {tool['description']}")
        
        # Test one tool call
        print(f"\n📰 Testing '{tools[0]['name']}' tool...")
        
        tool_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "search-news",
                "arguments": {
                    "query": "python programming",
                    "page_size": 1
                }
            }
        }
        
        process.stdin.write(json.dumps(tool_request) + "\n")
        process.stdin.flush()
        
        # Read tool response
        tool_response = process.stdout.readline()
        tool_data = json.loads(tool_response.strip())
        
        content = tool_data.get('result', {}).get('content', [])
        if content and content[0].get('text'):
            text = content[0]['text']
            lines = text.split('\n')
            print("✅ Tool Response:")
            print("-" * 30)
            for line in lines[:10]:  # Show first 10 lines
                print(line)
            if len(lines) > 10:
                print(f"... and {len(lines) - 10} more lines")
        
        # Cleanup
        process.terminate()
        process.wait()
        
        print(f"\n🎉 Local MCP server test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if process:
            process.terminate()

if __name__ == "__main__":
    test_single_request() 