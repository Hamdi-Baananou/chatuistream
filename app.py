import streamlit as st
from streamlit_extras.colored_header import colored_header
import streamlit.components.v1 as components

# Page configuration
st.set_page_config(
    page_title="ChatBot UI",
    page_icon="💬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    /* Main container padding */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Navbar styling */
    .navbar {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background-color: #ffffff;
        padding: 1rem 2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        z-index: 1000;
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 60px;
    }
    
    .company-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E1E1E;
        text-decoration: none;
        font-family: 'Arial', sans-serif;
        letter-spacing: 1px;
    }
    
    .extractor-button {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 20px;
        border: none;
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.3s ease;
        font-size: 1rem;
        position: fixed;
        right: 2rem;
        top: 1rem;
    }
    
    .extractor-button:hover {
        background-color: #45a049;
    }
    
    /* Chat input styling */
    .stTextInput > div > div > input {
        border-radius: 20px;
        padding: 10px 20px;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    
    .chat-message.user {
        background-color: #2b313e;
    }
    
    .chat-message.bot {
        background-color: #475063;
    }
    
    .chat-message .avatar {
        width: 20%;
    }
    
    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
    }
    
    /* Add padding to main content to account for fixed navbar */
    .main .block-container {
        padding-top: 5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Navbar
st.markdown("""
<div class="navbar">
    <div class="company-name">LEONI</div>
    <button class="extractor-button" onclick="document.querySelector('.extractor-button').click()">Extractor</button>
</div>
""", unsafe_allow_html=True)

# Extractor button functionality
if st.button("Extractor", key="extractor_btn", help="Open Extractor"):
    st.sidebar.title("Extractor")
    st.sidebar.write("Extractor functionality will be implemented here.")

# Welcome message
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1>Welcome to the ChatBot</h1>
        <p>How can I help you today?</p>
    </div>
    """, unsafe_allow_html=True)

# Chat input
user_input = st.text_input("", placeholder="Type your message here...", key="input")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        st.markdown(f"""
        <div class="chat-message {message['role']}">
            <div class="message">
                {message['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)

# Handle user input
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Add bot response (placeholder for now)
    st.session_state.messages.append({"role": "bot", "content": "This is a placeholder response. The actual chatbot functionality will be implemented later."})
    
    # Rerun to update the chat display
    st.rerun() 