"""
Graph exports for LangGraph Studio.
This file creates 3 separate graphs that can be visualized in LangGraph Studio.
"""

from src.langgraph_agenticai.graph.graph_builder import GraphBuilder
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Create a default LLM model
model = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile"
)

# User controls for graphs that need them
user_controls = {
    "tavily_api_key": TAVILY_API_KEY
}

# Graph 1: Basic Chatbot
# Simple conversational AI without external tools
builder_1 = GraphBuilder(model)
builder_1.basic_chatbot_graph()
basic_chatbot = builder_1.graph_builder.compile()

# Graph 2: Chatbot with Tools
# Enhanced chatbot with internet search capabilities
builder_2 = GraphBuilder(model)
builder_2.chatbot_with_tools()
chatbot_with_tools = builder_2.graph_builder.compile()

# Graph 3: AI News Pipeline
# Automated news fetching and summarization
builder_3 = GraphBuilder(model, user_controls)
builder_3.ai_news_builder()
ai_news_pipeline = builder_3.graph_builder.compile()


## Graph 4: Smart Router Graph
# Add this at the end of graphs.py
builder_unified = GraphBuilder(model, user_controls)
unified_router = builder_unified.create_unified_router_graph()
