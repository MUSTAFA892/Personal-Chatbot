---

# Personal Chatbot with Flask and React

This repository contains a chatbot application built with **Flask** (backend), **React** (frontend), and **LangChain** for a Retrieval-Augmented Generation (RAG) pipeline. The chatbot uses a **FAISS** vector store for efficient FAQ retrieval and **SQLite** for chat history storage, integrated with Google’s **Gemini LLM (gemini-1.5-flash)** for intelligent responses. The application is optimized for deployment on **Render**.

---

## 🚀 Features

* **Flask Backend**: REST API for processing user messages, managing chat history, and integrating with LangChain for RAG.
* **React Frontend**: Interactive UI for chatting with the bot, fetching responses from the Flask API.
* **LangChain RAG Pipeline**: Uses FAISS for vector search and Gemini LLM for generating context-aware responses based on a CSV FAQ dataset.
* **SQLite Database**: Stores chat history for retrieval via the `/history` endpoint.
* **Render Deployment**: Optimized for deployment on Render’s Starter plan, with pre-built FAISS index to avoid memory limits.

---

## 📚 Table of Contents

* [Flask Backend](#flask-backend)
* [React Frontend](#react-frontend)
* [LangChain RAG Integration](#langchain-rag-integration)
* [Project Structure](#project-structure)
* [Installation](#installation)
* [Usage](#usage)
* [Deployment on Render](#deployment-on-render)
* [Contributing](#contributing)
* [License](#license)

---

## 🧠 Flask Backend

### Overview

The Flask backend serves as the core of the chatbot, providing endpoints for:

* `/`: Welcome message.
* `/chat`: Process user messages and return bot responses using the RAG pipeline.
* `/history`: Retrieve the last 50 chat interactions from the SQLite database.

### Setup

1. **Install Dependencies**: Listed in `requirements.txt` (e.g., Flask, LangChain, FAISS).
2. **Configure Environment**: Set `GOOGLE_API_KEY` in `.env` for Gemini LLM access.
3. **Run the Backend**: Use Gunicorn for production or Flask’s development server locally.

---

## 💬 React Frontend

### Overview

The frontend is a React-based single-page application (e.g., `index.html` with embedded React) that provides an interactive chat interface. It communicates with the Flask backend via REST API calls to `/chat` and `/history`.

### Setup

* **Serve the Frontend**: Use a static file server (e.g., `python -m http.server`) or integrate into a larger React app.
* **Update API URL**: Configure the frontend to point to the Flask backend (e.g., `http://localhost:5000` or Render URL).

---

## 🔗 LangChain RAG Integration

### Overview

The `langchain_helper.py` script implements the RAG pipeline:

* **FAISS Vector Store**: Loads embeddings from `Data/Data.csv` for FAQ retrieval.
* **HuggingFace Embeddings**: Uses `all-MiniLM-L6-v2` for text embeddings.
* **Gemini LLM**: Generates responses based on retrieved FAQs.

### Functions

```python
from langchain_helper import get_qa_chain

chain = get_qa_chain()
response = chain.invoke({"query": "Who are you?"})
print(response["result"])  # Outputs response from FAQ or "I don't know."
```

* `create_vector_db()`: Generates the FAISS index from `Data/Data.csv`.
* `get_qa_chain()`: Loads the FAISS index and creates the RAG chain for querying.

---

## 📁 Project Structure

```
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
```

---

## ⚙️ Installation

### Prerequisites

* Python 3.10+
* `pip` for installing dependencies
* Git
* Google Cloud account with Gemini API key
* Node.js (optional, for advanced React setup)

### Steps

```bash
# Clone the Repository
git clone https://github.com/your-username/personal-chatbot.git
cd personal-chatbot

# Install Python Dependencies
pip install -r requirements.txt

# Set Up Environment Variables
echo "GOOGLE_API_KEY=your-gemini-api-key-here" > .env

# Generate FAISS Index
python langchain_helper.py

# Start the Flask Backend
python api.py

# Serve the React Frontend
cd frontend
python -m http.server 8000
```

Access at: [http://localhost:8000](http://localhost:8000)

---

## 💡 Usage

### Interact with the Chatbot

1. Open the React frontend in your browser.
2. Type a message (e.g., “Who are you?”) and submit.
3. The frontend sends the message to `/chat`, and the backend responds using the RAG pipeline.
4. The chat is saved in `chat.db`.

### Test API Endpoints

```bash
curl http://localhost:5000
curl -X POST -H "Content-Type: application/json" -d '{"message":"Who are you?"}' http://localhost:5000/chat
curl http://localhost:5000/history
```

### Update FAQs

1. Edit `Data/Data.csv`.
2. Regenerate the FAISS index:

```bash
rm -rf faiss_index
python langchain_helper.py
```

---

## ☁️ Deployment on Render

### Prerequisites

* Render account (Starter plan recommended)
* GitHub repository with project files
* Pre-built FAISS index committed to `faiss_index/`

### Steps

#### Prepare Repository

```bash
# Commit all changes (except .env and chat.db)
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

#### Create Web Service on Render

1. Log in to Render > **New > Web Service**
2. Connect GitHub repository
3. Configure:

* **Name**: `personal-chatbot`
* **Environment**: Python
* **Region**: Choose nearest
* **Branch**: main
* **Plan**: Starter (512MB RAM)
* **Build Command**: `pip install -r requirements.txt`
* **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 2 api:app`
* **Environment Variables**:

  * `GOOGLE_API_KEY`: Your Gemini API key
  * `PYTHON_VERSION`: 3.10
  * `WEB_CONCURRENCY`: 2

4. Click **Create Web Service**

#### Test Deployment

```bash
curl https://personal-chatbot.onrender.com/chat \
  -X POST -H "Content-Type: application/json" \
  -d '{"message":"Who are you?"}'
```

#### Update Frontend

Configure React frontend to use the Render URL:
`https://personal-chatbot.onrender.com`

---

### 🧠 Notes

* **Memory Optimization**: Pre-built FAISS index avoids memory issues. For lighter usage, switch to `paraphrase-MiniLM-L3-v2`.
* **FAISS Updates**: Regenerate and recommit `faiss_index/` after changes to `Data/Data.csv`.

---

## 🤝 Contributing

Contributions are welcome! You can help by:

* Reporting bugs or suggesting features
* Improving documentation or code efficiency
* Adding new FAQ entries to `Data/Data.csv`

### Steps

```bash
# Fork & Create Feature Branch
git checkout -b feature/your-feature

# Commit Changes
git commit -m "Add your feature"

# Push & Open PR
git push origin feature/your-feature
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
