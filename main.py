from agents.llm_agent import LLMAgent
from mcp_server.server import mcp
import asyncio
from fastmcp.client.transports import StdioTransport
from fastmcp.client import Client
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession


async def main(question):
    
    try:
        
        
        # stdio_transport = StdioTransport(
        #     command="python",
        #     args=["mcp_server/mcp_stdio.py"]
        # )
        
        # stdio_clinet = Client(stdio_transport)
        
        server_params = StdioServerParameters(
            command="python",
            args=["mcp_server/mcp_stdio.py"]
        )
        
        async with stdio_client(server_params) as (read, write, _sid):
            
            async with ClientSession(read,write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session) 
                agent = LLMAgent(tools)
                response = await agent.get_response(question)
                
            return response
                
        
        
    except ValueError as e:
            print(f"Value error: {e}")
            raise
            
    except Exception as e:
        print(f"Error in main: {e}")
        raise    


if __name__ == "__main__":
    
    question = input("Please give your query here")
    asyncio.run(main(question))