import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from langchain_helper import get_qa_chain

app = Flask(__name__)  # Create the Flask app instance
CORS(app)  # Enable CORS for cross-origin requests (React frontend)

# Initialize Database
def init_db():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            bot TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()  # Ensure DB is initialized

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Personal Chatbot API"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    # Get chatbot response
    chain = get_qa_chain()
    if chain is None:
        return jsonify({"error": "Failed to load QA chain"}), 500

    response = chain.invoke({"query": user_message})
    bot_response = response.get("result", "I don't know.")

    # Store in database
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (user, bot) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()
    conn.close()

    return jsonify({"user": user_message, "bot": bot_response}), 200

@app.route("/history", methods=["GET"])
def get_chat_history():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user, bot FROM chats ORDER BY id DESC LIMIT 50")
    chats = cursor.fetchall()
    conn.close()

    chat_history = [{"user": chat[0], "bot": chat[1]} for chat in chats]
    return jsonify(chat_history), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT isn't set
    print(f"Starting the app on port {port}")  # Debugging line to confirm the port
    app.run(host="0.0.0.0", port=port, debug=True)  # Use 'api' as the app instance
