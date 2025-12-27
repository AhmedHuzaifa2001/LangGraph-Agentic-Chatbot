from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
import os
from dotenv import load_dotenv
load_dotenv()

def get_tools():
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
    tools = [TavilySearchResults(max_results = 2)]
    return tools

def create_tool_node(tools):
    """
        creates and returns a tool node for the graph
    """
    return ToolNode(tools = tools)