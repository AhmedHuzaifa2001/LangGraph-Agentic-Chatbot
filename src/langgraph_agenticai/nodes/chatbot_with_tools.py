from src.langgraph_agenticai.state.state import *

class ChatbotToolNode:
    """
        Chatbot logic enhanced with tool integration
    """
    def __init__(self , model):
        self.llm = model

    def create_chatbot(self , tools): ## node method for chatbots with tools.
         """
        Returns a chatbot node function.
        """
         llm_with_tools = self.llm.bind_tools(tools)

         def chatbot_node(state:State):
             """
            Chatbot logic for processing the input state and returning a response.
            """
             return {"messages":[llm_with_tools.invoke(state["messages"])]}
         
         return chatbot_node