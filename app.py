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
# This needs to be processed before the UI that might depend on it is drawn,
# and before st.query_params is modified by other parts of the app on the same run.
if "action" in st.query_params:
    if st.query_params["action"] == "open_extractor":
        st.sidebar.title("Extractor")
        st.sidebar.write("Extractor functionality will be implemented here.")
        # Remove the action query parameter to prevent re-triggering on subsequent reruns
        # and to clean up the URL. This requires Streamlit 1.31+.
        # Modifying st.query_params implicitly triggers a rerun.
        del st.query_params["action"]
        # If using Streamlit < 1.31, you might need:
        # from streamlit.experimental import set_query_params
        # set_query_params() # Clears all query params

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
        padding: 1rem 2rem; /* Padding on left/right will affect visual centering if not accounted for */
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        z-index: 9999;
        display: flex;
        justify-content: center; /* Changed for centering */
        align-items: center;
        height: 60px;
        gap: 3rem; /* Added gap for spacing between centered items */
    }
    
    .company-name {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E1E1E;
        text-decoration: none;
        font-family: 'Arial', sans-serif;
        letter-spacing: 1px;
        /* Removed fixed positioning, z-index, top, left as it's now a flex item */
    }
    
    /* Hide the default Streamlit button (if any are still used and need hiding) */
    /* This rule might not be needed if no st.button is rendered that you want to hide. */
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
        /* Removed fixed positioning, z-index, top, right as it's now a flex item */
    }
    
    .extractor-button:hover {
        background-color: #45a049;
    }
    
    /* Ensure navbar is above all other content */
    .stApp > header {
        background-color: transparent;
        z-index: 9998;
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
        width: 20%; /* This seems large for an avatar, consider if this is intended */
    }
    
    .chat-message .message {
        width: 80%; /* If avatar is 20%, message is 80%. Check layout. */
                     /* If avatar is not used, message can be 100% */
        padding: 0 1.5rem; /* Original had this, but if there's no avatar div, this might be too much */
    }
    
    /* Add padding to main content to account for fixed navbar */
    .main .block-container {
        padding-top: 80px; /* Adjusted from 5rem to explicit px, ensure it's enough for 60px navbar */
    }
    
    /* Ensure content stays below navbar */
    .stApp > main {
        z-index: 1;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Navbar
# Updated onclick to set a query parameter and reload.
st.markdown("""
<div class="navbar">
    <div class="company-name">LEONI</div>
    <button class="extractor-button" onclick="
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('action', 'open_extractor');
        window.location.href = currentUrl.toString();
    ">Extractor</button>
</div>
""", unsafe_allow_html=True)

# The Streamlit button for "Extractor" is no longer needed here,
# as its functionality is triggered by the custom HTML button via query parameters.
# # Hidden button for functionality
# if st.button("Extractor", key="extractor_btn", help="Open Extractor"):
#     st.sidebar.title("Extractor") # This logic is now at the top, checking query_params
#     st.sidebar.write("Extractor functionality will be implemented here.")

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
        # Note: The original chat message HTML had an .avatar div and .message div structure.
        # If you're not using avatars, you might simplify this.
        # The current CSS sets .avatar to 20% width and .message to 80%.
        # If you only have message content, it might look off-center or too narrow.
        # For simplicity, I'll assume the message content should take full width within chat-message.
        st.markdown(f"""
        <div class="chat-message {message['role']}">
            <div class="message" style="width: 100%; padding: 0;"> 
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