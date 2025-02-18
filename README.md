
# Chatbot Project with Flask and Streamlit

This repository is a chatbot application built with **Flask** (for the backend) and **Streamlit** (for the frontend), integrated with **LangChain** for advanced NLP capabilities.

## Features

- **Flask Backend**: API handling for message processing, integrating LangChain for chatbot functionality.
- **Streamlit Frontend**: Interactive UI for chatting with the bot.
- **LangChain Integration**: NLP engine to generate intelligent responses.

## Table of Contents

- [Flask Backend](#flask-backend)
- [Streamlit Frontend](#streamlit-frontend)
- [LangChain Helper Integration](#langchain-helper-integration)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Flask Backend

### Overview
The Flask backend provides the server-side logic for the chatbot, handling user inputs and managing interactions with LangChain.

### Setup:
1. **Install Dependencies**:
   - Flask
   - LangChain (for chatbot responses)

2. **Run the Backend**:
   - Use `flask run` to start the backend server.

---

## Streamlit Frontend

### Overview
The Streamlit frontend provides an easy-to-use interface for users to interact with the chatbot.

### Setup:
1. **Install Dependencies**:
   - Streamlit (UI for the frontend)
   
2. **Run the Frontend**:
   - Use `streamlit run app.py` to start the frontend server.

---

## LangChain Helper Integration

### Overview
The `langchain_helper.py` script simplifies the integration of LangChain, providing a method for generating responses to user queries.

### Example Function:
```python
def get_chatbot_response(message):
    """
    Process the user message and get a response from LangChain.

    Arguments:
    message -- User input to be processed by LangChain.
    
    Returns:
    response -- The chatbot's response.
    """
    # LangChain integration code here
    return response
```

---

## Installation

### Prerequisites

Make sure you have Python 3.x installed on your machine. Also, ensure you have `pip` to install dependencies.

### Steps:
1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/chatbot-flask-streamlit.git
   cd chatbot-flask-streamlit
   ```

2. **Install Dependencies**:
   Install the required dependencies using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create the FAISS Index**:
   - Run the `langchain_helper.py` script to create the FAISS index used for chatbot response generation:
   ```bash
   python langchain_helper.py
   ```

4. **Start the Flask Backend**:
   Once the FAISS index is created, start the Flask backend:
   ```bash
   flask run
   ```

5. **Start the Streamlit Frontend**:
   Finally, run the Streamlit frontend:
   ```bash
   streamlit run app.py
   ```

---

## Usage

1. **Interact with the Chatbot**:
   - Open the Streamlit app in your browser (usually `http://localhost:8501`).
   - Type a message into the input field and click send.
   - The message is processed by the Flask backend and returned with a response from LangChain.

2. **LangChain Integration**:
   - The backend communicates with LangChain to generate intelligent responses based on user input.

---

## Contributing

We welcome contributions to the project! You can help by:
- Reporting bugs.
- Improving documentation.
- Adding new features or enhancements.

Feel free to fork the repository and create pull requests with your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
```

### Key Updates:
1. **FAISS Index Creation**: Added the step to run `langchain_helper.py` to create the FAISS index before starting Flask or Streamlit.
2. **`requirements.txt`**: Updated installation instructions to use `pip install -r requirements.txt` for installing dependencies.
3. **Ordering of Setup**: Included the step of creating the FAISS index before starting Flask and Streamlit, which is essential for the chatbot to function properly.

