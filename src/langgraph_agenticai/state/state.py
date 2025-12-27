from typing_extensions import TypedDict , Annotated
from langgraph.graph.message import add_messages



class State(TypedDict):
      
      """
    Represent the structure of the state used in graph
    """
      messages: Annotated[list , add_messages]
      news_data: list  
      summary: str    
      frequency: str  
        