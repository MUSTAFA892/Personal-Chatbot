import os
from flask import Flask, render_template, request, jsonify
import sqlite3
from langchain_helper import get_qa_chain

app = Flask(__name__)

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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Get chatbot response
    chain = get_qa_chain()
    response = chain.invoke({"query": user_message})
    bot_response = response["result"]

    # Store in database
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chats (user, bot) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()
    conn.close()

    return jsonify({"response": bot_response})

@app.route("/get_chat_history", methods=["GET"])
def get_chat_history():
    conn = sqlite3.connect("chat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user, bot FROM chats")
    chats = cursor.fetchall()
    conn.close()

    chat_history = [{"user": chat[0], "bot": chat[1]} for chat in chats]
    return jsonify(chat_history)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1000, debug=True)
