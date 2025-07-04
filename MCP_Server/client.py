# This should be able to interact with mathserver.py and weather.py
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

import asyncio

load_dotenv()

async def main():
    client = MultiServerMCPClient(
        {
            "math":{
                "command":"python", 
                "args":["mathserver.py"], #Ensure correct absolute path
                "transport":"stdio"
            },
            "weather":{
                "url":"http://localhost:8000/mcp", #Ensure server is running
                "transport":"streamable_http"
            }
        }
    )

    api_key = os.getenv("GROQ_API")
    tools = await client.get_tools()

    # Intialising the model
    model = ChatGroq(model = "qwen-qwq-32b", api_key = api_key)

    # Creating the agent
    agent = create_react_agent(
        model,tools
    )

    math_response = await agent.ainvoke(
        {"messages":[{"role":"user", "content":"What's (3+5) x 12?"}]}
    )

    print("Math response:", math_response['messages'][-1].content)

    weather_response = await agent.ainvoke(
        {"messages":[{"role":"user", "content":"What is the weather in Florida"}]}
    )

    print("Weather response", weather_response["messages"][-1].content)

asyncio.run(main())