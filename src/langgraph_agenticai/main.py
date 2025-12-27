import streamlit as st
from src.langgraph_agenticai.ui.streamlitui.loadui import LoadUI
from src.langgraph_agenticai.LLM.groqLLM import *
from src.langgraph_agenticai.graph.graph_builder import *
from src.langgraph_agenticai.ui.streamlitui.display_result import *

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
     
     

     if st.session_state.get("IsFetchButtonClicked", False):
          user_message = st.session_state.get("timeframe")
     else:
          user_message = st.chat_input("Enter your message: ")

     if user_message:
          try:
               llm_config =  GroqLLM(user_controls_input = user_input)
               model = llm_config.get_groq_llm()

               if not model:
                    st.error("Error: LLm Model could not be initialized")
               
               ## usecase setup

               usecase = user_input.get("selected_usecase")

               if not usecase:
                    st.error("Error: No usecase selected!!!")
               

               ##graph builder

               graph_builder = GraphBuilder(model)

               try:
                    graph = graph_builder.setup_graph(usecase)
                    DisplayResults(usecase , graph , user_message).display_result_on_ui()
               except Exception as e:
                    st.error(f"Error: Graph set up failed!!!: {e}")

          except Exception as e:
                st.error("Error: failed!!!: {e}")