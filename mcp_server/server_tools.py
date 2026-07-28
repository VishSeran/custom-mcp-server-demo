from mcp_server.server import MCPServer


mcp_server = MCPServer()
mcp = mcp_server.mcp_server

@mcp.tool
async def addition(a:float, b:float) -> float:
    
    try:
        if a is None or b is None:
            raise  ValueError("paramter a and b cannot be empty")
        
        return a + b
        
    except ValueError as e:
        print(f"Value error: {e}")
        raise
                
    except Exception as e:
        print(f"Error in llm agent init: {e}")
        raise
    
    
async def substract(a:float, b:float)