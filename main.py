from agents.llm_agent import LLMAgent
from mcp_server.server import mcp
import asyncio
from fastmcp.client.transports import StdioTransport
from fastmcp.client import Client


async def main():
    
    try:
        
        
        stdio_transport = StdioTransport(
            command="python",
            args=["mcp_server/mcp_stdio.py"]
        )
        
        stdio_clinet = Client(stdio_transport)
        
        
    except ValueError as e:
            print(f"Value error: {e}")
            raise
            
    except Exception as e:
        print(f"Error in main: {e}")
        raise    


if __name__ == "__main__":
    asyncio.run(main())