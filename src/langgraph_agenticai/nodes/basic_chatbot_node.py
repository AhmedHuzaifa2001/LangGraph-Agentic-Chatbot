from src.langgraph_agenticai.state.state import *

class Basic_chatbot_node:
    def __init__(self , model):
        self.llm = model

    def process(self , state:State) -> dict:
        return {"messages":self.llm.invoke(state["messages"])}

