import streamlit as st
from streamlit_extras.colored_header import colored_header # Not used, kept from original
import streamlit.components.v1 as components # Not used, kept from original
from streamlit.experimental import set_query_params # For clearing query params

# Page configuration
st.set_page_config(
    page_title="ChatBot UI",
    page_icon="💬",
    layout="wide"
)

# Initialize session state for drawer
if "drawer_open" not in st.session_state:
    st.session_state.drawer_open = False

# --- DEBUG PRINTS (check your terminal) ---
print(f"--- Top of Script ---")
print(f"Current st.query_params: {st.query_params}")
print(f"Current st.session_state.drawer_open: {st.session_state.drawer_open}")
# --- END DEBUG PRINTS ---

# Handle query params for drawer actions
if "drawer_action" in st.query_params:
    action = st.query_params.get("drawer_action") # Use .get() for safety
    
    # --- DEBUG PRINTS ---
    print(f"Found 'drawer_action': {action} in query_params.")
    # --- END DEBUG PRINTS ---

    if action == "open":
        st.session_state.drawer_open = True
    elif action == "close":
        st.session_state.drawer_open = False
    
    # --- DEBUG PRINTS ---
    print(f"After processing 'drawer_action', st.session_state.drawer_open: {st.session_state.drawer_open}")
    # --- END DEBUG PRINTS ---
    
    # Clear the query parameter to prevent re-triggering and clean URL.
    # This will cause a Streamlit rerun.
    set_query_params() # Clears ALL query parameters
    # If you have other query parameters you need to preserve, this approach needs refinement.
    # For Streamlit 1.31.0+ you could use:
    # del st.query_params["drawer_action"]
    # For this to take effect without set_query_params() explicitly calling rerun,
    # you might need to ensure the page reruns, e.g. st.rerun() if del doesn't trigger it
    # in some older compatible versions. However, set_query_params() is usually safer.

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
        z-index: 9999; /* Highest z-index */
        display: flex;
        justify-content: space-between; /* For left/right alignment */
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
    
    .stButton button {
        display: none; 
    }
    
    /* Custom button styling for navbar */
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
        display: inline-flex; 
        align-items: center;  
        gap: 0.5em;           
    }
    
    .extractor-button:hover {
        background-color: #45a049;
    }
    
    /* Streamlit's default header (if visible) */
    .stApp > header {
        background-color: transparent;
        z-index: 9998; /* Below our custom navbar */
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
    
    .chat-message .message {
        width: 100%; 
        padding: 0;  
    }
    
    /* Main content padding to account for fixed navbar */
    .main .block-container {
        padding-top: 80px; /* Ensure content starts below navbar */
    }
    
    /* Ensure main app content z-index is low */
    .stApp > main {
        z-index: 1;
    }

    /* Bottom Drawer Styling */
    .bottom-drawer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        height: calc(100vh - 60px); /* Full height minus navbar */
        background-color: #f8f9fa; /* Light background for the drawer */
        z-index: 9990; /* Below navbar (9999), above main content (1) and stApp>header (9998) */
        box-shadow: 0 -3px 10px rgba(0,0,0,0.15);
        transform: translateY(100%); /* Start off-screen (slid down) */
        transition: transform 0.3s ease-in-out;
        padding: 20px;
        box-sizing: border-box;
        overflow-y: auto; /* Allow scrolling for drawer content */
    }

    .bottom-drawer.open {
        transform: translateY(0); /* Slide into view */
    }

    .drawer-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 15px;
        border-bottom: 1px solid #e0e0e0;
        margin-bottom: 15px;
    }

    .drawer-header h2 {
        margin: 0;
        font-size: 1.5rem;
        color: #333;
    }

    .close-drawer-button {
        background-color: #e74c3c; /* Reddish color for close */
        color: white;
        padding: 0.4rem 1rem;
        border: none;
        border-radius: 15px; /* Rounded like navbar button */
        font-weight: 500;
        cursor: pointer;
        transition: background-color 0.3s ease;
        font-size: 0.9rem;
    }
    .close-drawer-button:hover {
        background-color: #c0392b;
    }
    .drawer-content {
        /* Style for the content area within the drawer */
        color: #333;
    }

</style>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- NAVBAR ---
# "Extractor" button now sets 'drawer_action=open'
st.markdown("""
<div class="navbar">
    <div class="company-name">LEONI</div>
    <button class="extractor-button" onclick="
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('drawer_action', 'open');
        window.location.href = currentUrl.toString();
    ">
        ✨ Extractor
    </button>
</div>
""", unsafe_allow_html=True)


# --- BOTTOM DRAWER ---
drawer_visibility_class = "open" if st.session_state.drawer_open else ""
# Prepare JavaScript for the close button in the drawer
close_button_onclick_js = """
    const currentUrlClose = new URL(window.location.href);
    currentUrlClose.searchParams.set('drawer_action', 'close');
    window.location.href = currentUrlClose.toString();
"""

# --- DEBUG PRINTS ---
print(f"Rendering drawer. st.session_state.drawer_open: {st.session_state.drawer_open}, drawer_visibility_class: '{drawer_visibility_class}'")
# --- END DEBUG PRINTS ---

st.markdown(f"""
<div class="bottom-drawer {drawer_visibility_class}">
    <div class="drawer-header">
        <h2>Extractor Details</h2>
        <button class="close-drawer-button" onclick="{close_button_onclick_js}">
            Close
        </button>
    </div>
    <div class="drawer-content">
        <p>This is where the content for the Extractor will be displayed.</p>
        <p>You can add more specific functionality, forms, or data visualizations here later.</p>
        <p>For example, you might embed another Streamlit component or custom HTML content.</p>
        <!-- Your custom drawer content will go here -->
    </div>
</div>
""", unsafe_allow_html=True)


# --- MAIN CHAT INTERFACE ---

# Welcome message (only if no chat messages yet)
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1>Welcome to the ChatBot</h1>
        <p>How can I help you today?</p>
    </div>
    """, unsafe_allow_html=True)

# Chat input
user_input = st.text_input("", placeholder="Type your message here...", key="input_main_chat") 

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
    # Clear the input field after processing by rerunning
    st.rerun()