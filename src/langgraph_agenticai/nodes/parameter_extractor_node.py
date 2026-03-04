from src.langgraph_agenticai.state.state import State
from pydantic import BaseModel , Field
from langchain_core.prompts import ChatPromptTemplate


class ExtractedParameters(BaseModel):
    frequency: str = Field(
        description="Time period: daily, weekly, monthly, or year"
    )

    confidence: str = Field(
        description="high, medium, or low confidence in extraction"
    )


class ParameterExtractorNode:
    def __init__(self, llm):
        self.llm = llm

    def extract_params(self, state: State):
       
        usecase = state.get("usecase", "")
        
        if usecase != "ai_news":
           
            return {}
        
        # Extract user query for ai_news
        latest_message = state["messages"][-1]
        
        if isinstance(latest_message, dict):
            user_query = latest_message.get('content', '')
        else:
            user_query = latest_message.content

        # Create extraction prompt
        system_prompt = """Extract the time period from the user's request.
                Valid periods: daily, weekly, monthly, year
                If not specified, default to 'weekly'."""

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{user_query}")
            ]
        )

        # Use LLM to extract parameters
        llm_with_structure = self.llm.with_structured_output(ExtractedParameters)
        extracted = llm_with_structure.invoke(prompt.format_messages(user_query=user_query))

      
        return {
            "frequency": extracted.frequency
        }
