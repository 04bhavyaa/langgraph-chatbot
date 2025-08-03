import os
import logging
from typing import TypedDict, Annotated, Dict, Any
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatState(TypedDict):
    """State definition for the chat graph"""
    messages: Annotated[list[BaseMessage], add_messages]


class LangGraphChatbot:
    """Simplified LangGraph chatbot"""
    
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        """Initialize the chatbot"""
        # Validate API key
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Initialize LLM
        self.llm = ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.7,
            max_tokens=2048
        )
        
        # Initialize checkpointer
        self.checkpointer = MemorySaver()
        
        # Build the graph
        self._build_graph()
        
        logger.info(f"Chatbot initialized with model: {model_name}")
    
    def _build_graph(self) -> None:
        """Build the conversation graph"""
        graph = StateGraph(ChatState)
        graph.add_node("chat_node", self._chat_node)
        graph.add_edge(START, "chat_node")
        graph.add_edge("chat_node", END)
        
        self.chatbot = graph.compile(checkpointer=self.checkpointer)
    
    def _chat_node(self, state: ChatState) -> Dict[str, Any]:
        """Process messages and generate response"""
        try:
            messages = state.get('messages', [])
            response = self.llm.invoke(messages)
            
            if not isinstance(response, AIMessage):
                response = AIMessage(content=str(response))
            
            return {'messages': [response]}
            
        except Exception as e:
            logger.error(f"Error in chat node: {e}")
            error_response = AIMessage(
                content=f"Sorry, I encountered an error: {str(e)}"
            )
            return {'messages': [error_response]}
    
    def get_response(self, user_input: str, config: Dict[str, Any]) -> str:
        """Get response from the chatbot"""
        try:
            input_messages = [HumanMessage(content=user_input)]
            
            result = self.chatbot.invoke(
                {'messages': input_messages}, 
                config=config
            )
            
            messages = result.get('messages', [])
            if messages and hasattr(messages[-1], 'content'):
                return messages[-1].content
            else:
                return "I couldn't generate a response."
                
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return f"Error: {str(e)}"


# Create global chatbot instance
try:
    chatbot = LangGraphChatbot()
except Exception as e:
    logger.error(f"Failed to create chatbot: {e}")
    chatbot = None