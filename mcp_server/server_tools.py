mcp = MCPServer()

async def addition(a:float, b:float) -> float:
    
    try:
        if not a or b:
            raise ValueError("paramter a and b cannot be empty")
        
        
    except ValueError as e:
        print(f"Value error: {e}")
        raise
                
    except Exception as e:
        print(f"Error in llm agent init: {e}")
        raise