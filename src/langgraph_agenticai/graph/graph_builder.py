from langgraph.graph import StateGraph , START , END
from src.langgraph_agenticai.state.state import *
from src.langgraph_agenticai.nodes.basic_chatbot_node import *
from src.langgraph_agenticai.tools.search_tool import *
from langgraph.prebuilt import tools_condition , ToolNode
from src.langgraph_agenticai.nodes.chatbot_with_tools import *
from src.langgraph_agenticai.nodes.ai_news_node import *
from src.langgraph_agenticai.nodes.router_node import RouterNode
from src.langgraph_agenticai.nodes.parameter_extractor_node import ParameterExtractorNode

class GraphBuilder:
    def __init__(self , model, user_controls=None):
        self.llm = model
        self.user_controls = user_controls or {}
        self.graph_builder = StateGraph(State)



    def route_to_usecase(self , state:State) -> str:

        """
    Determines which usecase node to route to based on state.
    Returns the name of the next node.
    """
        
        usecase = state.get("usecase" , "basic_chatbot")

        if usecase == "ai_news":
            return "fetch_news"
        elif usecase == "chatbot_with_tools":
            return "chatbot_with_tools"
        else:
            return "basic_chatbot"
        


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

        tavily_key = self.user_controls.get("tavily_api_key")
        ai_news = AINewsNode(self.llm, tavily_api_key=tavily_key)
        self.graph_builder.add_node("fetch_news" , ai_news.fetch_news)
        self.graph_builder.add_node("summarize_news" , ai_news.summarize_news)
        self.graph_builder.add_node("save_results" , ai_news.save_result)

     
        self.graph_builder.set_entry_point("fetch_news")  ## this is like START --> fetch_news
        self.graph_builder.add_edge("fetch_news" , "summarize_news")
        self.graph_builder.add_edge("summarize_news" , "save_results")
        self.graph_builder.add_edge("save_results" , END)


    
    def create_unified_router_graph(self):
        """
        Creates a unified graph with automatic routing based on query intent.
        Flow: START → router → parameter_extractor → [conditional routing to usecase] → END
        """
        # Create a FRESH StateGraph for the unified router
        unified_graph = StateGraph(State)
        
        router = RouterNode(self.llm)
        extractor = ParameterExtractorNode(self.llm)

        # Add router and extractor nodes
        unified_graph.add_node("router", router.route_query)
        unified_graph.add_node("parameter_extractor", extractor.extract_params)

        # ===== Add Basic Chatbot Node =====
        basic_chatbot_node = Basic_chatbot_node(self.llm)
        unified_graph.add_node("basic_chatbot", basic_chatbot_node.process)

        # ===== Add Chatbot with Tools Nodes =====
        tools = get_tools()
        tools_node = create_tool_node(tools)
        chatbot_tool_obj = ChatbotToolNode(self.llm)
        chatbot_with_tools_node = chatbot_tool_obj.create_chatbot(tools)
        
        unified_graph.add_node("chatbot_with_tools", chatbot_with_tools_node)
        unified_graph.add_node("tools", tools_node)

        # ===== Add AI News Nodes =====
        tavily_key = self.user_controls.get("tavily_api_key")
        ai_news = AINewsNode(self.llm, tavily_api_key=tavily_key)
        
        unified_graph.add_node("fetch_news", ai_news.fetch_news)
        unified_graph.add_node("summarize_news", ai_news.summarize_news)
        unified_graph.add_node("save_results", ai_news.save_result)

        # ===== Connect the Flow =====
        # START → router → parameter_extractor
        unified_graph.add_edge(START, "router")
        unified_graph.add_edge("router", "parameter_extractor")

        # Conditional routing from parameter_extractor based on usecase
        unified_graph.add_conditional_edges(
            "parameter_extractor",
            self.route_to_usecase,  # This function returns the next node name
            {
                "basic_chatbot": "basic_chatbot",
                "chatbot_with_tools": "chatbot_with_tools",
                "fetch_news": "fetch_news"
            }
        )

        # ===== Wire Each Usecase to END =====
        # Basic chatbot → END
        unified_graph.add_edge("basic_chatbot", END)

        # Chatbot with tools → tools (conditional) → chatbot_with_tools → END
        unified_graph.add_conditional_edges(
            "chatbot_with_tools",
            tools_condition,  # Built-in LangGraph function
            {
                "tools": "tools",
                "__end__": END
            }
        )
        unified_graph.add_edge("tools", "chatbot_with_tools")
        
        # AI News pipeline → END
        unified_graph.add_edge("fetch_news", "summarize_news")
        unified_graph.add_edge("summarize_news", "save_results")
        unified_graph.add_edge("save_results", END)

        return unified_graph.compile()

        





    def setup_graph(self , usecase):
        """
        Builds the graph for the selected use case (old system - manual selection).
        Does NOT compile — caller is responsible for calling graph_builder.compile().
        """

        if usecase == "Basic Chatbot":
            self.basic_chatbot_graph()

        elif usecase == "Chatbot With Web":
            self.chatbot_with_tools()

        elif usecase == "AI News":
            self.ai_news_builder()