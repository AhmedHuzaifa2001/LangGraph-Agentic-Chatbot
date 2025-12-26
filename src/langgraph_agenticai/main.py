import streamlit as st
from src.langgraph_agenticai.ui.streamlitui.loadui import LoadUI


def load_agentic_app():
     
     """
      Loads and runs the LangGraph AgenticAI application with Streamlit UI.
      This function initializes the UI, handles user input, configures the LLM model,
      sets up the graph based on the selected use case, and displays the output while 
      implementing exception handling for robustness.

    """
     ## LoadUI
     ui = LoadUI()
     user_input = ui.load_ui()

     if not user_input:
          st.error("Error : Failed to load user input")
     
     user_message = st.chat_input("Enter your message: ")
     
     