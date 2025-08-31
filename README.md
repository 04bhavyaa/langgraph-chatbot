# LangGraph Chatbot

A simple Streamlit-based AI assistant powered by LangGraph and Google Gemini.

## Features

- Conversational AI using LangGraph and Gemini
- Clean, familiar chat UI (no streaming)
- Session-based chat history
- Easy to reset conversation

## Setup Instructions

1. **Clone the repository**

   ```sh
   git clone https://github.com/04bhavyaa/langgraph-chatbot.git
   cd langgraph-chatbot
   ```

2. **Install dependencies**

   ```sh
   pip install -r requirements.txt
   ```

3. **Set your Google API Key**

   - Create a `.env` file in the project root:
     ```env
     GOOGLE_API_KEY=your-google-api-key-here
     ```

4. **Run the app**
   ```sh
   streamlit run streamlit_frontend.py
   ```

## Troubleshooting

- If the app spins forever or shows "Chatbot unavailable", check your `GOOGLE_API_KEY` and internet connection.
- Make sure all dependencies in `requirements.txt` are installed.
- For debugging, check the logs in the terminal and Streamlit UI.

## File Structure

- `langgraph_backend.py` — Backend logic for LangGraph chatbot
- `streamlit_frontend.py` — Streamlit UI for chat
- `requirements.txt` — Python dependencies
- `.env` — Your API key (not committed)

## License

MIT
