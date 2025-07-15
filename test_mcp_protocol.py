#!/usr/bin/env python3
"""
Test the MCP protocol interface directly
"""

import json
import subprocess
import sys
import os

def test_mcp_protocol():
    """Test the MCP server via its protocol interface"""
    
    print("🧪 Testing MCP Protocol Interface")
    print("=" * 50)
    
    # Test with the actual module
    cmd = [sys.executable, "-m", "src.news_api_mcp"]
    
    try:
        # Start the MCP server process
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.path.dirname(__file__)
        )
        
        # Test 1: Initialize
        print("📡 Test 1: Initializing MCP connection...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send initialization
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()
        
        # Read response
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(f"✅ Init Response: {response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
        
        # Test 2: List tools
        print("\n🔧 Test 2: Listing tools...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        process.stdin.write(json.dumps(list_tools_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            tools = response.get('result', {}).get('tools', [])
            print(f"✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool.get('name')}: {tool.get('description')}")
        
        # Test 3: Call a tool
        print("\n📰 Test 3: Calling search-news tool...")
        call_tool_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "search-news",
                "arguments": {
                    "query": "technology",
                    "page_size": 2
                }
            }
        }
        
        process.stdin.write(json.dumps(call_tool_request) + "\n")
        process.stdin.flush()
        
        response_line = process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            content = response.get('result', {}).get('content', [])
            if content:
                text = content[0].get('text', '')
                lines = text.split('\n')[:5]  # First 5 lines
                print("✅ Tool response (first 5 lines):")
                for line in lines:
                    print(f"   {line}")
                print("   ...")
        
        # Clean up
        process.terminate()
        process.wait()
        
        print("\n🎉 MCP Protocol test complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if process:
            process.terminate()
            process.wait()

if __name__ == "__main__":
    test_mcp_protocol() 