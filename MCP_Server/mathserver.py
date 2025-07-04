from mcp.server.fastmcp import FastMCP

# intialising the server
mcp = FastMCP("Math") #server name

@mcp.tool()
def add(a:int, b:int)->int:
    """_summary_
    add two numbers
    """
    return a+b

@mcp.tool()
def multiply(a:int, b:int)-> int:
    """_summary_
    multiply two numbers
    """
    return a*b



