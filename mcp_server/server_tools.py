
from mcp_server.server import mcp


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
        print(f"Error in addition: {e}")
        raise
    
@mcp.tool
async def substract(a:float, b:float):
    
    try:
            if a is None or b is None:
                raise  ValueError("paramter a and b cannot be empty")
            
            return a - b
            
    except ValueError as e:
        print(f"Value error: {e}")
        raise
                
    except Exception as e:
        print(f"Error in substraction: {e}")
        raise
    

@mcp.tool
async def multiply(a:float, b:float):
    
    try:
            if a is None or b is None:
                raise  ValueError("paramter a and b cannot be empty")
            
            return a * b
            
    except ValueError as e:
        print(f"Value error: {e}")
        raise
                
    except Exception as e:
        print(f"Error in multiplication: {e}")
        raise
    
@mcp.tool
async def division(a:float, b:float):
    
    try:
            if a is None or b is None:
                raise  ValueError("paramter a and b cannot be empty")
            
            if b == 0:
                raise ValueError("paramter b cannot be zero")
            
            return a/b
            
    except ValueError as e:
        print(f"Value error: {e}")
        raise
                
    except Exception as e:
        print(f"Error in llm agent init: {e}")
        raise
    
if __name__ == "__main__":
    
    mcp.run()