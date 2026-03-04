import streamlit as st
from langchain_core.messages import HumanMessage , AIMessage , ToolMessage
import json

class DisplayResults:
    def __init__(self , usecase , graph , user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    
    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message

        # Smart Router - dynamically handles all usecases
        if usecase == "Smart Router":
            with st.chat_message("user"):
                st.write(user_message)
            
            for event in graph.stream({"messages": [HumanMessage(content=user_message)]}):
                for value in event.values():
                    # Guard against None or non-dict stream events
                    if not isinstance(value, dict):
                        continue

                    # Show which route was chosen (for debugging/transparency)
                    if "usecase" in value:
                        st.info(f"🤖 Routed to: **{value['usecase']}**")
                    
                    if "messages" in value:
                        msgs = value["messages"]
                        # Normalise to list
                        if not isinstance(msgs, list):
                            msgs = [msgs]
                        message = msgs[-1] if msgs else None
                        
                        # Handle AI responses
                        if isinstance(message, AIMessage):
                            if hasattr(message, 'tool_calls') and message.tool_calls:
                                with st.chat_message("assistant"):
                                    st.write(f"🔧 Using tools: {[tool['name'] for tool in message.tool_calls]}")
                            else:
                                with st.chat_message("assistant"):
                                    st.write(message.content)
                        
                        elif isinstance(message, ToolMessage):
                            with st.expander("Tool Result"):
                                st.write(message.content)
                    
                    # Handle AI News summary
                    if "summary" in value:
                        with st.chat_message("assistant"):
                            st.markdown("### 📰 AI News Summary")
                            st.markdown(value["summary"])
                        if "filename" in value:
                            st.success(f"✅ Summary saved to: `{value['filename']}`")

        elif usecase == "Basic Chatbot":
            for event in graph.stream({"messages":[HumanMessage(content=user_message)]}):
                    
                    print(event.values())
                    for value in event.values():
                            print(value['messages'])
                            with st.chat_message("user"):
                                st.write(user_message)
                            with st.chat_message("assistant"):
                                st.write(value["messages"].content)


        elif usecase == "Chatbot With Web":
            with st.chat_message("user"):
                st.write(user_message)
            
            for event in graph.stream({"messages": [HumanMessage(content=user_message)]}):
                for value in event.values():
                    if "messages" in value:
                        message = value["messages"][-1]  # Get the latest message
                        
                        # Handle AI responses
                        if isinstance(message, AIMessage):
                            # Check if it has tool calls
                            if hasattr(message, 'tool_calls') and message.tool_calls:
                                with st.chat_message("assistant"):
                                    st.write(f"🔧 Using tools: {[tool['name'] for tool in message.tool_calls]}")
                            else:
                                # Final AI response without tool calls
                                with st.chat_message("assistant"):
                                    st.write(message.content)
                        
                        # Handle Tool responses (optional - show tool results)
                        elif isinstance(message, ToolMessage):
                            with st.expander("Tool Result"):
                                st.write(message.content)
        

        elif usecase == "AI News":

            with st.spinner("🔍 Fetching and summarizing latest AI news..."):
                result = None
                for event in graph.stream({"messages": [HumanMessage(content=user_message)]}):
                    for value in event.values():
                        result = value
                
                # Display the final summary
                if result and "summary" in result:
                    with st.chat_message("assistant"):
                        st.markdown("### 📰 AI News Summary")
                        st.markdown(result["summary"])
                    
                    # Show save location if available
                    if "filename" in result:
                        st.success(f"✅ Summary saved to: `{result['filename']}`")
                else:
                    st.error("❌ Failed to fetch news. Please try again.")
