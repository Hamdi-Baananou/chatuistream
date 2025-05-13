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
    .main {
        padding: 0rem 1rem;
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
    .chat-message .avatar {
        width: 20%;
    }
    .chat-message .message {
        width: 80%;
        padding: 0 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Navbar
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("<h1 style='text-align: left;'>Company Name</h1>", unsafe_allow_html=True)
with col2:
    if st.button("Extractor"):
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