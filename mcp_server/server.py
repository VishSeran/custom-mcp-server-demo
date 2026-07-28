from fastmcp import FastMCP

from configs.logger import get_logger


logger = get_logger("server")


class MCPServer:
    
    def __init__(self):
        
        
        self.mcp_server = FastMCP(
            name="CalculatorMCPServer",
            instructions="""
                This server facilitates different tools to process the calculation operations.
                including addition, substraction, multiplication and division 
            """
        )

mcp_server = MCPServer()
mcp = mcp_server.mcp_server