import streamlit as st
import os
from src.langgraph_agenticai.ui.uiconfig import Config


class LoadUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_ui(self):
             
             st.set_page_config(
                 page_title= self.config.get_page_title(), 
                 layout="wide",
                 page_icon="🤖",
                 initial_sidebar_state="expanded"
             )
             
             # Enhanced header with gradient effect using custom CSS
             st.markdown("""
                <style>
                .main-header {
                    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                    padding: 2rem;
                    border-radius: 10px;
                    text-align: center;
                    color: white;
                    font-size: 2.5rem;
                    font-weight: bold;
                    margin-bottom: 2rem;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                .sidebar-info {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1rem;
                    border-radius: 8px;
                    color: white;
                    margin-bottom: 1.5rem;
                    text-align: center;
                }
                </style>
                <div class="main-header">
                    🤖 """ + self.config.get_page_title() + """
                </div>
             """, unsafe_allow_html=True)
             
             # Welcome message in main area
             col1, col2, col3 = st.columns([1, 2, 1])
             with col2:
                 st.info("💡 Configure your AI agent in the sidebar and start chatting below!")

             with st.sidebar:
                # Sidebar header with styling
                st.markdown("""
                    <div class="sidebar-info">
                        <h3>⚙️ Configuration Panel</h3>
                        <p>Customize your AI experience</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Get options from config
                llm_options = self.config.get_llm_options()
                usecase_options = self.config.get_usecase_options()

                # LLM selection with icon
                st.markdown("### 🧠 AI Model Selection")
                self.user_controls["selected_llm"] = st.selectbox(
                    "Choose LLM Provider", 
                    llm_options,
                    help="Select the Large Language Model provider"
                )
                
                st.divider()

                if self.user_controls["selected_llm"] == "Groq":
                    st.markdown("### ⚡ Groq Configuration")
                    model_options = self.config.get_groq_model_options()
                    self.user_controls["selected_groq_model"] = st.selectbox(
                        "Model Version", 
                        model_options,
                        help="Select the specific Groq model"
                    )
                    
                    self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input(
                        "🔑 API Key",
                        type="password",
                        help="Enter your Groq API key"
                    )
                    
                    # Enhanced validation with better styling
                    if not self.user_controls["GROQ_API_KEY"]:
                        st.warning("⚠️ Please enter your GROQ API key to proceed.")
                    else:
                        st.success("✅ API Key configured!")
                
                st.divider()
                
                # Usecase selection with icon
                st.markdown("### 🎯 Use Case Selection")
                self.user_controls["selected_usecase"] = st.selectbox(
                    "Choose Application Type",
                    usecase_options,
                    help="Select the use case for your AI agent"
                )
                

                ## Chatbot usecase selection
                if self.user_controls["selected_usecase"] == "Chatbot With Web" or self.user_controls["selected_usecase"] == "AI News":
                     
                     self.user_controls["tavily_api_key"] = st.session_state["tavily_api_key"] = st.text_input("Tavily Api Key" , type = "password")

                     if not self.user_controls["tavily_api_key"]:
                          st.warning("Please enter your Tavily Api Key!!!")



                ## AI News usecase selection
                if self.user_controls["selected_usecase"] == "AI News":
                     st.subheader("AI News Explorer")

                     with st.sidebar:
                          time_frame = st.selectbox(
                               "select time frame",
                               ["Daily" , "Weekly" , "Monthly"],
                               index = 0
                          )
                     if st.button("Fetch Latest AI News" , use_container_width = True):
                          st.session_state.IsFetchButtonClicked = True  ## Creates a flag (boolean) in session state
                          st.session_state.timeframe = time_frame
                     


                # Footer with additional info
                st.divider()
                st.markdown("""
                    <div style='text-align: center; color: #666; font-size: 0.8rem;'>
                        <p>🚀 Powered by LangGraph</p>
                        <p>📊 Build Stateful AI Agents</p>
                    </div>
                """, unsafe_allow_html=True)
                
             return self.user_controls