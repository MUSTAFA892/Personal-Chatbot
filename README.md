Personal Chatbot with Flask and React
This repository contains a chatbot application built with Flask (backend), React (frontend), and LangChain for a Retrieval-Augmented Generation (RAG) pipeline. The chatbot uses a FAISS vector store for efficient FAQ retrieval and SQLite for chat history storage, integrated with Google’s Gemini LLM (gemini-1.5-flash) for intelligent responses. The application is optimized for deployment on Render.
Features

Flask Backend: REST API for processing user messages, managing chat history, and integrating with LangChain for RAG.
React Frontend: Interactive UI for chatting with the bot, fetching responses from the Flask API.
LangChain RAG Pipeline: Uses FAISS for vector search and Gemini LLM for generating context-aware responses based on a CSV FAQ dataset.
SQLite Database: Stores chat history for retrieval via the /history endpoint.
Render Deployment: Optimized for deployment on Render’s Starter plan, with pre-built FAISS index to avoid memory limits.

Table of Contents

Flask Backend
React Frontend
LangChain RAG Integration
Project Structure
Installation
Usage
Deployment on Render
Contributing
License


Flask Backend
Overview
The Flask backend serves as the core of the chatbot, providing endpoints for:

/: Welcome message.
/chat: Process user messages and return bot responses using the RAG pipeline.
/history: Retrieve the last 50 chat interactions from the SQLite database.

Setup

Install Dependencies: Listed in requirements.txt (e.g., Flask, LangChain, FAISS).
Configure Environment: Set GOOGLE_API_KEY in .env for Gemini LLM access.
Run the Backend: Use Gunicorn for production or Flask’s development server locally.


React Frontend
Overview
The frontend is a React-based single-page application (e.g., index.html with embedded React) that provides an interactive chat interface. It communicates with the Flask backend via REST API calls to /chat and /history.
Setup

Serve the Frontend: Use a static file server (e.g., python -m http.server) or integrate into a larger React app.
Update API URL: Configure the frontend to point to the Flask backend (e.g., http://localhost:5000 or Render URL).


LangChain RAG Integration
Overview
The langchain_helper.py script implements the RAG pipeline:

FAISS Vector Store: Loads embeddings from Data/Data.csv for FAQ retrieval.
HuggingFace Embeddings: Uses all-MiniLM-L6-v2 for text embeddings.
Gemini LLM: Generates responses based on retrieved FAQs.
Functions:
create_vector_db(): Generates the FAISS index from Data/Data.csv.
get_qa_chain(): Loads the FAISS index and creates the RAG chain for querying.



Example Usage
from langchain_helper import get_qa_chain

chain = get_qa_chain()
response = chain.invoke({"query": "Who are you?"})
print(response["result"])  # Outputs response from FAQ or "I don't know."


Project Structure
├── Data
│   └── Data.csv              # FAQ dataset for RAG pipeline
├── faiss_index
│   ├── index.faiss           # Pre-built FAISS index
│   ├── index.pkl             # FAISS metadata
├── static                    # Static assets (if used)
├── templates                 # HTML templates (if used)
├── api.py                    # Flask backend
├── langchain_helper.py       # LangChain RAG pipeline
├── .env                      # Environment variables (not committed)
├── chat.db                   # SQLite database (not committed)
├── requirements.txt          # Python dependencies
├── render.yaml               # Render deployment config (optional)
├── README.md                 # Project documentation


Installation
Prerequisites

Python 3.10+
pip for installing dependencies
Git for cloning the repository
Google Cloud account with Gemini API key
Node.js (optional, for advanced React setup)

Steps

Clone the Repository:
git clone https://github.com/your-username/personal-chatbot.git
cd personal-chatbot


Install Python Dependencies:
pip install -r requirements.txt


Set Up Environment Variables:Create a .env file in the project root:
GOOGLE_API_KEY=your-gemini-api-key-here

Replace your-gemini-api-key-here with your Gemini API key from Google Cloud Console.

Generate FAISS Index:Run langchain_helper.py to create the FAISS index:
python langchain_helper.py

This generates faiss_index/index.faiss and faiss_index/index.pkl.

Start the Flask Backend:
python api.py

The server runs at http://localhost:5000.

Serve the React Frontend:Save index.html (or your React app) in a frontend/ directory and serve it:
cd frontend
python -m http.server 8000

Access at http://localhost:8000.



Usage

Interact with the Chatbot:

Open the React frontend in your browser (e.g., http://localhost:8000).
Type a message (e.g., “Who are you?”) and submit.
The frontend sends the message to /chat, which retrieves a response via the RAG pipeline and stores it in chat.db.
View chat history via the /history endpoint.


Test API Endpoints:
curl http://localhost:5000
curl -X POST -H "Content-Type: application/json" -d '{"message":"Who are you?"}' http://localhost:5000/chat
curl http://localhost:5000/history


Update FAQs:

Edit Data/Data.csv with new prompt-response pairs.
Regenerate the FAISS index:rm -rf faiss_index
python langchain_helper.py






Deployment on Render
Prerequisites

Render account (Starter plan recommended, 512MB RAM)
GitHub repository with project files
Pre-built FAISS index committed to faiss_index/

Steps

Prepare Repository:

Commit all files except .env and chat.db (use .gitignore from artifact version 0f6bad51-c0bd-4a0c-a65b-e2234b2c1dc1).
Push to GitHub:git add .
git commit -m "Prepare for Render deployment"
git push origin main




Create Web Service on Render:

Log in to Render and click New > Web Service.
Connect your GitHub repository.
Configure:
Name: personal-chatbot
Environment: Python
Region: Choose a close region (e.g., Frankfurt)
Branch: main
Plan: Starter (512MB RAM)
Build Command: pip install -r requirements.txt
Start Command: gunicorn --bind 0.0.0.0:$PORT --workers 2 api:app
Environment Variables:
GOOGLE_API_KEY: Your Gemini API key
PYTHON_VERSION: 3.10
WEB_CONCURRENCY: 2




Click Create Web Service.


Test Deployment:

Get the Render URL (e.g., https://personal-chatbot.onrender.com).
Test API endpoints:curl https://personal-chatbot.onrender.com/chat -X POST -H "Content-Type: application/json" -d '{"message":"Who are you?"}'




Update Frontend:

Configure the React frontend to use the Render URL (e.g., https://personal-chatbot.onrender.com).



Notes

Memory Optimization: The FAISS index is pre-built locally to avoid Render’s memory limits. If memory issues persist, use a lighter embedding model (paraphrase-MiniLM-L3-v2) or upgrade to the Standard plan (1GB RAM).
FAISS Updates: Regenerate and recommit faiss_index/ if Data/Data.csv changes.


Contributing
Contributions are welcome! You can help by:

Reporting bugs or suggesting features.
Improving documentation or code efficiency.
Adding new FAQ entries to Data/Data.csv.

To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.


License
This project is licensed under the MIT License. See the LICENSE file for details.
