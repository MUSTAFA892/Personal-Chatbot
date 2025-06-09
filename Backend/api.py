import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from langchain_helper import get_qa_chain
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Verify Gemini API key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set. Ensure it is defined in the .env file or environment.")

# Initialize Database
def init_db():
    with sqlite3.connect("chat.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT NOT NULL,
                bot TEXT NOT NULL
            )
        """)
        conn.commit()

init_db()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Personal Chatbot API"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        if not user_message:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Get chatbot response
        chain = get_qa_chain()
        if chain is None:
            print("Error: QA chain initialization failed")
            return jsonify({"error": "Failed to load QA chain"}), 500

        response = chain.invoke({"query": user_message})
        bot_response = response.get("result", "I don't know.")

        # Store in database
        with sqlite3.connect("chat.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO chats (user, bot) VALUES (?, ?)", (user_message, bot_response))
            conn.commit()

        return jsonify({"user": user_message, "bot": bot_response}), 200

    except Exception as e:
        print(f"Error in /chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route("/history", methods=["GET"])
def get_chat_history():
    try:
        with sqlite3.connect("chat.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user, bot FROM chats ORDER BY id DESC LIMIT 50")
            chats = cursor.fetchall()

        chat_history = [{"user": chat[0], "bot": chat[1]} for chat in chats]
        return jsonify(chat_history), 200

    except Exception as e:
        print(f"Error in /history endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting the app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=False)