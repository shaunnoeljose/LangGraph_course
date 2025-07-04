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

"""
transport = "studio" argument tells the server to:
use standard input/output (stdin and stdout) to recieve and respond to tool function calls. Helps to test things locally. 
"""

if __name__ == "__main__":
    mcp.run(transport="stdio")



