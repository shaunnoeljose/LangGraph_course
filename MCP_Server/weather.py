from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather_function(location:str)->str:
    """
    get the weather location
    """
    return "Its always raining in Florida"

if __name__ == "__main__":
    mcp.run(transport = "streamable-http") #can setup the port to run the service



