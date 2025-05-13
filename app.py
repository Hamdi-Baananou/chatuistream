import streamlit as st
from streamlit_extras.colored_header import colored_header # Not used in this snippet, but kept from original
import streamlit.components.v1 as components # Not used in this snippet, but kept from original

# Page configuration
st.set_page_config(
    page_title="ChatBot UI",
    page_icon="💬",
    layout="wide"
)

# Handle query params for actions FIRST (e.g., opening the extractor)
if "action" in st.query_params:
    if st.query_params["action"] == "open_extractor":
        st.sidebar.title("Extractor")
        st.sidebar.write("Extractor functionality will be implemented here.")
        del st.query_params["action"] # Requires Streamlit 1.31+

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
        padding: 1rem 2rem; /* Padding on left/right creates space from edges */
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        z-index: 9999;
        display: flex;
        justify-content: space-between; /* Changed for left/right alignment */
        align-items: center;
        height: 60px;
        /* gap: 3rem; Removed as space-between handles main distribution */
    }
    
    .company-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E1E1E;
        text-decoration: none;
        font-family: 'Arial', sans-serif;
        letter-spacing: 1px;
    }
    
    .stButton button {
        display: none; 
    }
    
    /* Custom button styling */
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
        display: inline-flex; /* Added for icon alignment */
        align-items: center;  /* Added for icon alignment */
        gap: 0.5em;           /* Added for space between icon and text */
    }
    
    .extractor-button:hover {
        background-color: #45a049;
    }
    
    .stApp > header {
        background-color: transparent;
        z-index: 9998;
    }
    
    .stTextInput > div > div > input {
        border-radius: 20px;
        padding: 10px 20px;
    }
    
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
    
    .chat-message .message {
        width: 100%; /* Ensuring message takes full width within its container */
        padding: 0;  /* Adjust if specific padding is needed for message content */
    }
    
    .main .block-container {
        padding-top: 80px; 
    }
    
    .stApp > main {
        z-index: 1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Navbar
# HTML elements reordered: button first (left), then company name (right)
# Added ✨ icon to the button
st.markdown("""
<div class="navbar">
    <button class="extractor-button" onclick="
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('action', 'open_extractor');
        window.location.href = currentUrl.toString();
    ">
        ✨ Extractor
    </button>
    <div class="company-name">LEONI</div>
</div>
""", unsafe_allow_html=True)

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
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.messages.append({"role": "bot", "content": "This is a placeholder response. The actual chatbot functionality will be implemented later."})
    st.rerun()