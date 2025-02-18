import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = "http://localhost:5000"; // Replace with your backend's base URL

function App() {
  const [userMessage, setUserMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadChatHistory();
  }, []);

  // Load the chat history from the backend API
  const loadChatHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/history`);
      const data = await response.json();
      setChatHistory(data);
    } catch (error) {
      console.error('Error loading chat history:', error);
    }
  };

  // Send a message to the backend and get a response
  const sendMessage = async () => {
    if (!userMessage.trim()) return;

    // Append user message to chat
    const updatedChatHistory = [...chatHistory, { user: userMessage, bot: '' }];
    setChatHistory(updatedChatHistory);
    setUserMessage('');
    document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;

    setLoading(true);

    try {
      const response = await fetch(`${API_BASE_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage })
      });

      const data = await response.json();
      const botMessage = data.bot || "I don't know.";

      // Update the chat with the bot's response
      updatedChatHistory[updatedChatHistory.length - 1].bot = botMessage;
      setChatHistory(updatedChatHistory);
      setLoading(false);
      document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;
    } catch (error) {
      console.error('Error sending message:', error);
      setLoading(false);
    }
  };

  return (
    <div className="wrapper">
      <div className="title">Let's Chat</div>
      <div className="box" id="chat-box">
        {chatHistory.map((chat, index) => (
          <React.Fragment key={index}>
            <div className="item user">
              <div className="msg">{chat.user}</div>
            </div>
            <div className="item bot">
              <div className="msg">{chat.bot}</div>
            </div>
          </React.Fragment>
        ))}
        {loading && (
          <div className="item bot">
            <div className="msg">...</div>
          </div>
        )}
      </div>

      <div className="typing-area">
        <div className="input-field">
          <input
            type="text"
            id="user-input"
            placeholder="Type your message..."
            value={userMessage}
            onChange={(e) => setUserMessage(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                sendMessage();
              }
            }}
          />
        </div>
        <button id="send-button" onClick={sendMessage}>
          <i className="fa fa-paper-plane"></i> Send
        </button>
      </div>
    </div>
  );
}

export default App;
