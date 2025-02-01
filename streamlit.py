import streamlit as st
from langchain_helper import get_qa_chain, create_vector_db

# Custom CSS styling
st.markdown("""
<style>
    .main {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    .sidebar .sidebar-content {
        background-color: #2d2d2d;
    }
    .stTextInput textarea {
        color: #ffffff !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        color: white !important;
        background-color: #3d3d3d !important;
    }

    .stSelectbox svg {
        fill: white !important;
    }

    .stSelectbox option {
        background-color: #2d2d2d !important;
        color: white !important;
    }

    div[role="listbox"] div {
        background-color: #2d2d2d !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# Set the title of the app
st.title("Personal Chatbot🌱")


# Initialize session state for message history if not already initialized
if "message_log" not in st.session_state:
    st.session_state.message_log = [{"role": "ai", "content": "Hi! How can I help you today? 😊"}]

# Display chat messages
for message in st.session_state.message_log:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for user question
user_query = st.chat_input("Ask a question")

# Process the input when the user submits a question
if user_query:
    # Add the user's message to the message log
    st.session_state.message_log.append({"role": "user", "content": user_query})

    # Get the QA chain and run it
    chain = get_qa_chain()
    response = chain.invoke({"query": user_query})
    answer = response["result"]

    # Add AI's response to the message log
    st.session_state.message_log.append({"role": "ai", "content": answer})

    # Rerun to update the chat window with the new conversation
    st.rerun()
