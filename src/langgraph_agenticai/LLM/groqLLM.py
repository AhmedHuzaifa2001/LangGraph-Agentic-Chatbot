import streamlit as st
import os
from langchain_groq import ChatGroq


class GroqLLM:
    def __init__(self , user_controls_input):
        self.user_control_inputs = user_controls_input

    def get_groq_llm(self):
        try:
            groq_api_key = self.user_control_inputs["GROQ_API_KEY"]
            selected_groq_model = self.user_control_inputs["selected_groq_model"]

            if groq_api_key == "":
                st.error("Please enter the Groq API Key!!!")
                return None
        
            llm = ChatGroq(api_key = groq_api_key , model = selected_groq_model)

        except Exception as e:
            raise ValueError(f"Error occurred: {e}")
        
        return llm
        
