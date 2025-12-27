from langgraph.graph import StateGraph , START , END
from src.langgraph_agenticai.state.state import *
from src.langgraph_agenticai.nodes.basic_chatbot_node import *
from src.langgraph_agenticai.tools.search_tool import *
from langgraph.prebuilt import tools_condition , ToolNode
from src.langgraph_agenticai.nodes.chatbot_with_tools import *
from src.langgraph_agenticai.nodes.ai_news_node import *

class GraphBuilder:
    def __init__(self , model):
        self.llm = model
        self.graph_builder = StateGraph(State)


    def basic_chatbot_graph(self):

        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """
        
        self.basic_chatbot_node = Basic_chatbot_node(self.llm)

        self.graph_builder.add_node("chatbot" , self.basic_chatbot_node.process)

        self.graph_builder.add_edge(START , "chatbot")
        self.graph_builder.add_edge("chatbot" , END)



    def chatbot_with_tools(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node 
        and a tool node. It defines tools, initializes the chatbot with tool 
        capabilities, and sets up conditional and direct edges between nodes. 
        The chatbot node is set as the entry point.
        """
        ## Define the tool and toolNode
        tools = get_tools()
        tools_node = create_tool_node(tools)

        llm = self.llm

        chatbot_tool_obj = ChatbotToolNode(llm)
        chatbot_node = chatbot_tool_obj.create_chatbot(tools)

        ## Add nodes
        self.graph_builder.add_node("chatbot" , chatbot_node)
        self.graph_builder.add_node("tools" , tools_node)

        self.graph_builder.add_edge(START , "chatbot")
        self.graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition
        )
        self.graph_builder.add_edge("tools" , "chatbot")



    def ai_news_builder(self):

        ai_news = AINewsNode(self.llm)
        self.graph_builder.add_node("fetch_news" , ai_news.fetch_news)
        self.graph_builder.add_node("summarize_news" , ai_news.summarize_news)
        self.graph_builder.add_node("save_results" , ai_news.save_result)

     
        self.graph_builder.set_entry_point("fetch_news")  ## this is like START --> fetch_news
        self.graph_builder.add_edge("fetch_news" , "summarize_news")
        self.graph_builder.add_edge("summarize_news" , "save_results")
        self.graph_builder.add_edge("save_results" , END)

    def setup_graph(self , usecase):
        """
        setup the graph for the selected use case
        """

        if usecase == "Basic Chatbot":
            self.basic_chatbot_graph()

        elif usecase == "Chatbot With Web":
            self.chatbot_with_tools()

        elif usecase == "AI News":
            self.ai_news_builder()
        
        return self.graph_builder.compile()
        