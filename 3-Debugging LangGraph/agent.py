from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import END, START
from langgraph.graph.state import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API")
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "test_project"

# initalise LLM
llm = ChatGroq(model = "llama3-70b-8192", api_key = groq_api_key)

# Defining State
class State(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages] #keeps the list of all the messages added

# Defining tool 
def make_tool_graph():

    @tool
    def add(a:float, b:float)->float:
        """
        Add two numbers

        """
        return a+b

    tools = add
    tool_node = ToolNode([tools])

    # binding the llm
    llm_with_tool = llm.bind_tools([add])

    # Defining node
    def call_llm(state:State):
        return {"messages":[llm_with_tool.invoke(state["messages"])]}

    # Building Graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("call_llm", call_llm)
    graph_builder.add_node("tools", tool_node)

    # Adding edges
    graph_builder.add_edge(START,"call_llm")
    graph_builder.add_conditional_edges("call_llm", tools_condition)
    graph_builder.add_edge("tools","call_llm")

    graph= graph_builder.compile()   
    return graph

tool_agent = make_tool_graph()