import streamlit as st
from langchain_core.messages import HumanMessage , AIMessage , ToolMessage
import json

class DisplayResults:
    def __init__(self , usecase , graph , user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    
    def _render_history(self):
        for message in st.session_state.get("messages", []):
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.write(message.content)

            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.write(message.content)

            elif isinstance(message, ToolMessage):
                with st.expander("Tool Result"):
                    st.write(message.content)


    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph

        self._render_history()

        if usecase == "Smart Router":
            final_ai_message = None

            for event in graph.stream({"messages": st.session_state["messages"]}):
                for value in event.values():
                    if not isinstance(value, dict):
                        continue

                    if "usecase" in value:
                        st.info(f"Routed to: {value['usecase']}")

                    if "messages" in value:
                        msgs = value["messages"]
                        if not isinstance(msgs, list):
                            msgs = [msgs]

                        message = msgs[-1] if msgs else None

                        if isinstance(message, AIMessage):
                            final_ai_message = message
                            if hasattr(message, "tool_calls") and message.tool_calls:
                                with st.chat_message("assistant"):
                                    st.write(f"Using tools: {[tool['name'] for tool in message.tool_calls]}")
                            elif message.content:
                                with st.chat_message("assistant"):
                                    st.write(message.content)

                        elif isinstance(message, ToolMessage):
                            with st.expander("Tool Result"):
                                st.write(message.content)

                    if "summary" in value:
                        with st.chat_message("assistant"):
                            st.markdown("### AI News Summary")
                            st.markdown(value["summary"])
                        final_ai_message = AIMessage(content=value["summary"])

            if final_ai_message and final_ai_message.content:
                if not st.session_state["messages"] or st.session_state["messages"][-1] != final_ai_message:
                    st.session_state["messages"].append(final_ai_message)

        elif usecase == "Basic Chatbot":
            final_ai_message = None

            for event in graph.stream({"messages": st.session_state["messages"]}):
                for value in event.values():
                    if isinstance(value, dict) and "messages" in value:
                        msgs = value["messages"]
                        if not isinstance(msgs, list):
                            msgs = [msgs]

                        message = msgs[-1] if msgs else None

                        if isinstance(message, AIMessage):
                            final_ai_message = message
                            with st.chat_message("assistant"):
                                st.write(message.content)

            if final_ai_message and final_ai_message.content:
                st.session_state["messages"].append(final_ai_message)

        elif usecase == "Chatbot With Web":
            final_ai_message = None

            for event in graph.stream({"messages": st.session_state["messages"]}):
                for value in event.values():
                    if "messages" in value:
                        message = value["messages"][-1]

                        if isinstance(message, AIMessage):
                            final_ai_message = message
                            if hasattr(message, "tool_calls") and message.tool_calls:
                                with st.chat_message("assistant"):
                                    st.write(f"Using tools: {[tool['name'] for tool in message.tool_calls]}")
                            else:
                                with st.chat_message("assistant"):
                                    st.write(message.content)

                        elif isinstance(message, ToolMessage):
                            with st.expander("Tool Result"):
                                st.write(message.content)

            if final_ai_message and final_ai_message.content:
                st.session_state["messages"].append(final_ai_message)

        elif usecase == "AI News":
            with st.spinner("Fetching and summarizing latest AI news..."):
                result = None

                for event in graph.stream({"messages": st.session_state["messages"]}):
                    for value in event.values():
                        result = value

                if result and "summary" in result:
                    with st.chat_message("assistant"):
                        st.markdown("### AI News Summary")
                        st.markdown(result["summary"])

                    st.session_state["messages"].append(AIMessage(content=result["summary"]))

                    if "filename" in result:
                        st.success(f"Summary saved to: {result['filename']}")
                else:
                    st.error("Failed to fetch news. Please try again.")