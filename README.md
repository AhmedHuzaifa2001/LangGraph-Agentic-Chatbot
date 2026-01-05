# LangGraph Agentic Chat-Bot

A modular and extensible chatbot application built with LangGraph and Streamlit, featuring multiple use cases including basic chat, tool-integrated chat, and AI news aggregation.

## 🚀 Features

- **Multiple Chat Modes**
  - Basic Chatbot: Simple conversational interface
  - Chatbot with Tools: Enhanced with external tool integration
  - AI News: Automated news fetching and summarization

- **LLM Integration**
  - Groq API support with multiple model options
  - Configurable model selection through UI

- **Interactive UI**
  - Built with Streamlit for responsive web interface
  - Real-time chat interaction
  - Customizable configuration via INI files

- **Graph-Based Architecture**
  - Powered by LangGraph for stateful conversations
  - Modular node-based design for easy extensibility

## 📁 Project Structure

```
LangGraph-chatbot/
├── app.py                          # Application entry point
├── README.md                       # Project documentation
├── AINews/                         # AI news summaries storage
│   ├── weekly_summary.md
│   └── monthly_summary.md
└── src/
    └── langgraph_agenticai/
        ├── main.py                 # Main application logic
        ├── graph/                  # Graph construction
        │   └── graph_builder.py
        ├── LLM/                    # LLM integrations
        │   └── groqLLM.py
        ├── nodes/                  # Node implementations
        │   ├── ai_news_node.py
        │   ├── basic_chatbot_node.py
        │   └── chatbot_with_tools.py
        ├── state/                  # State management
        │   └── state.py
        ├── tools/                  # Tool integrations
        │   └── search_tool.py
        └── ui/                     # UI components
            ├── uiconfig.ini
            ├── uiconfig.py
            └── streamlitui/
                ├── loadui.py
                └── display_result.py
```


## 🎯 Use Cases

### 1. Basic Chatbot
Simple conversational AI without external tools. Ideal for general queries and conversations.

### 2. Chatbot with Tools
Enhanced chatbot with internet search capabilities using Tavily API. Perfect for information retrieval and fact-checking.

### 3. AI News
Automated AI news aggregation with configurable timeframes (Daily/weekly/monthly). Fetches and summarizes latest AI developments.

## ⚙️ Configuration

Edit `src/langgraph_agenticai/ui/uiconfig.ini` to customize:

- Page title
- Available LLM options
- Use case selections
- Groq model choices

Example:
```ini
[DEFAULT]
PAGE_TITLE = LangGraph Agentic ChatBot
LLM_OPTIONS = Groq , OpenAI
USECASE_OPTIONS = Basic Chatbot , Chatbot with Tools , AI News
GROQ_MODEL_OPTIONS = llama-3.1-70b-versatile , mixtral-8x7b-32768
```

## 🏗️ Architecture

The application follows a modular architecture:

1. **Graph Builder**: Constructs the conversation flow based on selected use case
2. **Nodes**: Individual processing units (chatbot, tools, news fetcher)
3. **State Management**: Maintains conversation context using TypedDict
4. **UI Layer**: Streamlit-based interface for user interaction
5. **LLM Integration**: Groq API for language model inference
