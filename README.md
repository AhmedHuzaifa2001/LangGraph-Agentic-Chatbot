# 🤖 LangGraph Agentic Chatbot

A modular, extensible agentic chatbot built with **LangGraph**, **LangChain**, and **Streamlit**. Features an LLM-powered Smart Router that automatically classifies user intent and routes queries to specialized agents — no manual mode switching needed.

---

## 🚀 Features

### 🔀 Smart Router (Unified Agent)
- **LLM-powered intent classification** using Pydantic structured output — automatically detects whether a query needs general chat, web search, or AI news
- **Parameter extraction** — for AI news queries, a second LLM pass extracts the time period (daily/weekly/monthly/year) from natural language
- **Conditional graph routing** — seamlessly routes to the correct sub-agent without user intervention

### 💬 Basic Chatbot
- Direct conversational AI using Groq LLMs
- Supports multi-turn conversations with full message history

### 🌐 Chatbot with Web Search
- Enhanced chatbot with **Tavily web search** tool integration
- LangGraph's built-in `tools_condition` for automatic tool invocation
- Displays tool calls and results in expandable UI sections

### 📰 AI News Pipeline
- **3-stage automated pipeline**: Fetch → Summarize → Save
- Fetches up to 20 articles via Tavily's news search API
- LLM-generated markdown summaries sorted by date (IST timezone)
- Saves output to `./AINews/{frequency}_summary.md`
- Configurable timeframes: Daily, Weekly, Monthly, Yearly

### 💾 In-Session Chat History
- Full conversation memory within a session via `st.session_state`
- Multi-turn context — the LLM sees the entire conversation, not just the latest message
- Chat history rendering on every Streamlit rerun
- **Clear Chat** button to reset the conversation

### 🖥️ LangGraph Studio Integration
- 4 pre-compiled graphs exported for visual debugging and exploration in LangGraph Studio
- Configured via `langgraph.json`

---

## 📁 Project Structure

```
LangGraph-chatbot/
├── app.py                              # Application entry point
├── graphs.py                           # LangGraph Studio graph exports (4 graphs)
├── langgraph.json                      # LangGraph Studio configuration
├── README.md                           # Project documentation
├── AINews/                             # Generated news summary outputs
│   ├── daily_summary.md
│   ├── weekly_summary.md
│   ├── monthly_summary.md
│   └── year_summary.md
└── src/
    └── langgraph_agenticai/
        ├── __init__.py
        ├── main.py                     # App orchestrator — UI, LLM, graph setup, display
        │
        ├── graph/
        │   └── graph_builder.py        # Graph construction for all 4 use cases
        │
        ├── nodes/
        │   ├── basic_chatbot_node.py   # Simple LLM chat node
        │   ├── chatbot_with_tools.py   # Tool-augmented chat node (closure pattern)
        │   ├── ai_news_node.py         # 3-step news pipeline (fetch/summarize/save)
        │   ├── router_node.py          # LLM-based intent classifier (structured output)
        │   └── parameter_extractor_node.py  # Extracts time period for AI news queries
        │
        ├── state/
        │   └── state.py                # Unified TypedDict state (messages, news_data, summary, frequency, usecase)
        │
        ├── tools/
        │   └── search_tool.py          # Tavily web search tool + ToolNode factory
        │
        ├── LLM/
        │   └── groqLLM.py              # Groq LLM provider wrapper
        │
        └── ui/
            ├── uiconfig.ini            # Externalized UI configuration
            ├── uiconfig.py             # INI config parser
            └── streamlitui/
                ├── loadui.py           # Sidebar config panel + main area layout
                └── display_result.py   # Per-usecase result rendering with chat history
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Streamlit UI                           │
│  ┌──────────────┐  ┌────────────────────────────────────┐   │
│  │   Sidebar     │  │         Chat Interface              │  │
│  │  - LLM Config │  │  - Message history rendering       │  │
│  │  - Use Case   │  │  - Streaming graph events          │  │
│  │  - API Keys   │  │  - Tool call display               │  │
│  │  - Clear Chat │  │  - News summary rendering          │  │
│  └──────────────┘  └────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  main.py    │
                    │ Orchestrator│
                    └──────┬──────┘
                           │
              ┌────────────▼────────────┐
              │     GraphBuilder        │
              │  (4 graph constructors) │
              └────────────┬────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         │                 │                  │
    Manual Select    Smart Router       LangGraph Studio
    (setup_graph)   (unified graph)     (graphs.py)
         │                 │
         │    ┌────────────▼────────────┐
         │    │   Router Node (LLM)     │
         │    │   Intent Classification │
         │    └────────────┬────────────┘
         │                 │
         │    ┌────────────▼────────────┐
         │    │  Parameter Extractor    │
         │    │  (AI News time period)  │
         │    └────────────┬────────────┘
         │                 │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────────┐
    │             │                  │
┌───▼───┐  ┌─────▼─────┐  ┌────────▼────────┐
│ Basic │  │ Chat +    │  │  AI News        │
│ Chat  │  │ Tools     │  │  Pipeline       │
│       │  │  ↕ Tavily │  │ Fetch→Summ→Save │
└───────┘  └───────────┘  └─────────────────┘
```

---

## 🎯 Use Cases

### 1. Smart Router (Recommended)
The unified agent that handles everything. Type any query and the LLM-powered router automatically detects your intent:
- **General questions** → routes to Basic Chatbot
- **Current info / web search** → routes to Chatbot with Tools
- **AI news requests** → routes to AI News Pipeline (with automatic time period extraction)

Uses Pydantic `BaseModel` with `with_structured_output()` for reliable, typed classification.

### 2. Basic Chatbot
Simple conversational AI without external tools. Ideal for general queries, opinions, and conversations.

### 3. Chatbot with Web Search
Enhanced chatbot with Tavily web search integration. Uses LangGraph's `tools_condition` for automatic tool invocation. Perfect for questions requiring current information.

### 4. AI News
Automated AI news aggregation with configurable timeframes. Fetches the latest AI news globally, summarizes it into structured markdown, and saves the output to files.

---

## ⚙️ Configuration

### UI Configuration
Edit `src/langgraph_agenticai/ui/uiconfig.ini` to customize:

```ini
[DEFAULT]
PAGE_TITLE = LangGraph: Build Stateful Agentic AI LangGraph
LLM_OPTIONS = Groq
USECASE_OPTIONS = Smart Router , Basic Chatbot , Chatbot With Web , AI News
GROQ_MODEL_OPTIONS = llama-3.3-70b-versatile , llama-3.1-8b-instant , meta-llama/llama-guard-4-12b , openai/gpt-oss-120b
```

### Required API Keys
| Key | Required For | Where to Get |
|-----|-------------|--------------|
| **Groq API Key** | All use cases | [console.groq.com](https://console.groq.com) |
| **Tavily API Key** | Chatbot with Web, AI News, Smart Router | [tavily.com](https://tavily.com) |

API keys are entered through the Streamlit sidebar at runtime.

---

## 🧠 Available Models

| Model | Description |
|-------|-------------|
| `llama-3.3-70b-versatile` | High-quality, versatile Llama 3.3 (70B parameters) |
| `llama-3.1-8b-instant` | Fast, lightweight Llama 3.1 (8B parameters) |
| `meta-llama/llama-guard-4-12b` | Safety-focused Llama Guard 4 (12B parameters) |
| `openai/gpt-oss-120b` | Open-source GPT model (120B parameters) |

All models are served via **Groq** for ultra-fast inference.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Groq API key
- Tavily API key (for web search and news features)

### Installation

```bash
# Clone the repository
git clone https://github.com/AhmedHuzaifa2001/LangGraph-Agentic-Chatbot.git
cd LangGraph-chatbot

# Install dependencies
pip install -r requirements.txt

# (Optional) Create a .env file for LangGraph Studio
echo "GROQ_API_KEY=your_key_here" > .env
echo "TAVILY_API_KEY=your_key_here" >> .env
```

### Run the App

```bash
streamlit run app.py
```

### LangGraph Studio (Optional)
To visualize and debug graphs in LangGraph Studio, ensure `langgraph.json` and `.env` are configured, then open the project in LangGraph Studio.

---

## 🔧 Tech Stack

| Technology | Purpose |
|------------|---------|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful graph orchestration for agentic workflows |
| [LangChain](https://github.com/langchain-ai/langchain) | LLM abstractions, prompt templates, message types |
| [Groq](https://groq.com) | Ultra-fast LLM inference (Llama models) |
| [Tavily](https://tavily.com) | Web search API and news fetching |
| [Streamlit](https://streamlit.io) | Interactive web UI framework |
| [Pydantic](https://docs.pydantic.dev) | Structured LLM output validation |

---

## 📊 Graph Visualizations (LangGraph Studio)

The project exports 4 compiled graphs for LangGraph Studio:

| Graph | Description |
|-------|-------------|
| `basic_chatbot` | START → chatbot → END |
| `chatbot_with_tools` | START → chatbot ↔ tools → END (conditional) |
| `ai_news_pipeline` | fetch_news → summarize_news → save_results → END |
| `unified_router` | START → router → parameter_extractor → [conditional routing] → sub-agent → END |

---

## 🗂️ State Schema

All graphs share a unified `State` (TypedDict):

```python
class State(TypedDict):
    messages: Annotated[list, add_messages]   # Conversation history (auto-accumulated)
    news_data: list                            # Raw Tavily search results
    summary: str                               # LLM-generated news summary
    frequency: str                             # Time period (daily/weekly/monthly/year)
    usecase: Literal["basic_chatbot", "chatbot_with_tools", "ai_news"]
    extracted_params: str                      # Extracted parameters from user query
```

---

## 📝 Key Design Patterns

- **Dual Routing System** — Manual dropdown selection (old) + LLM-powered Smart Router (new) coexist
- **Structured Output** — Router and parameter extractor use `with_structured_output()` with Pydantic models for typed, reliable classification
- **Closure Pattern** — `ChatbotToolNode.create_chatbot(tools)` returns a closure that captures the tool-bound LLM
- **INI-based Config** — UI options externalized to `uiconfig.ini` for easy customization without code changes
- **Session State Management** — `st.session_state` for in-session chat history persistence and UI flags
- **InMemorySaver Checkpointer** — Smart Router graph uses LangGraph's `InMemorySaver` for graph state checkpointing

---

## 🛣️ Roadmap

- [ ] Persistent chat history with `SqliteSaver` checkpointer (survive browser refreshes)
- [ ] Conversation sidebar with past chat threads
- [ ] Streaming responses (token-by-token)
- [ ] RAG — chat with uploaded documents
- [ ] Multi-provider LLM support (OpenAI, Anthropic, Ollama)
- [ ] LangSmith observability integration
- [ ] Docker deployment

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute.
