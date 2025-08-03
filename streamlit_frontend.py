import streamlit as st
import uuid
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the chatbot
try:
    from langgraph_backend import chatbot
    CHATBOT_AVAILABLE = chatbot is not None
except ImportError as e:
    logger.error(f"Failed to import chatbot: {e}")
    CHATBOT_AVAILABLE = False
    chatbot = None

# Page configuration
st.set_page_config(
    page_title="LangGraph AI Assistant",
    page_icon="🤖",
    layout="centered"
)


def initialize_session():
    """Initialize session state"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'thread_id' not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())


def clear_chat():
    """Clear chat history"""
    st.session_state.messages = []
    st.session_state.thread_id = str(uuid.uuid4())
    st.rerun()


def get_chat_config():
    """Get LangGraph configuration"""
    return {'configurable': {'thread_id': st.session_state.thread_id}}


def main():
    """Main application"""
    initialize_session()
    
    # Header
    st.title("LangGraph based AI Assistant")
    
    # Check if chatbot is available
    if not CHATBOT_AVAILABLE:
        st.error("❌ Chatbot unavailable. Check your GOOGLE_API_KEY and dependencies.")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("Controls")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
        
        st.divider()
        st.header("Stats")
        st.metric("Messages", len(st.session_state.messages))
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            try:
                # Show thinking indicator
                with st.spinner("Thinking..."):
                    config = get_chat_config()
                    response = chatbot.get_response(prompt, config)
                
                # Display the complete response
                st.markdown(response)
                
                # Add to session state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response
                })
                
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_msg
                })
    
    # Welcome message for new users
    if len(st.session_state.messages) == 0:
        st.info("👋 Welcome! Ask me anything to get started.")


if __name__ == "__main__":
    main()