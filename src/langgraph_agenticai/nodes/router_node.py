from src.langgraph_agenticai.state.state import State
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field


class RouteClassification(BaseModel):
        usecase: str = Field(description="The classified usecase: basic_chatbot, chatbot_with_tools, or ai_news")
        reasoning: str = Field(description="Brief explanation of why this usecase was chosen")

class RouterNode:

    def __init__(self , llm):
        self.llm = llm

  

    def route_query(self , state:State):
        # Extract user query first
        latest_message = state["messages"][-1]
        
        if isinstance(latest_message, dict):
            user_query = latest_message.get('content', '')
        else:
            user_query = latest_message.content

       
        system_prompt = """You are a routing agent. Classify user queries into ONE of these categories:

        - basic_chatbot: General questions, greetings, opinions, historical facts
        - chatbot_with_tools: Queries needing current info or web search (sports, weather, recent events)
        - ai_news: Requests for AI news, trends, updates, summaries

        Respond with the appropriate usecase and brief reasoning."""

       
        prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{user_query}"),
            ]
        )

        # Get classification with structured output
        llm_with_structure = self.llm.with_structured_output(RouteClassification)
        classification = llm_with_structure.invoke(prompt_template.format_messages(user_query=user_query))
        
        
        return {"usecase": classification.usecase}
