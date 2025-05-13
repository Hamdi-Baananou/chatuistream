import streamlit as st
# from streamlit_extras.colored_header import colored_header # Not used in this snippet
# import streamlit.components.v1 as components # Not used in this snippet

# Page configuration
st.set_page_config(
    page_title="ChatBot UI",
    page_icon="💬",
    layout="wide"
)

# Initialize session state for drawer
if "drawer_open" not in st.session_state:
    st.session_state.drawer_open = False

# Handle query params for drawer actions
if "drawer_action" in st.query_params:
    action = st.query_params.get("drawer_action") 

    if action == "open":
        st.session_state.drawer_open = True
    elif action == "close":
        st.session_state.drawer_open = False
    
    # Remove the query parameter and rerun
    if "drawer_action" in st.query_params: # Check again as st.query_params is a new dict on rerun
        del st.query_params["drawer_action"]
    
    st.rerun()

# Custom CSS and JavaScript functions
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
        color: #333;
    }
</style>
<script>
    function openExtractorDrawer() {
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('drawer_action', 'open');
        window.location.href = currentUrl.toString();
    }

    function closeExtractorDrawer() {
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('drawer_action', 'close');
        window.location.href = currentUrl.toString();
    }
</script>
""", unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- NAVBAR ---
# "Extractor" button now calls the JavaScript function openExtractorDrawer()
st.markdown("""
<div class="navbar">
    <div class="company-name">LEONI</div>
    <button class="extractor-button" onclick="openExtractorDrawer()">
        ✨ Extractor
    </button>
</div>
""", unsafe_allow_html=True)


# --- BOTTOM DRAWER ---
drawer_visibility_class = "open" if st.session_state.drawer_open else ""

# The "Close" button now calls the JavaScript function closeExtractorDrawer()
st.markdown(f"""
<div class="bottom-drawer {drawer_visibility_class}">
    <div class="drawer-header">
        <h2>Extractor Details</h2>
        <button class="close-drawer-button" onclick="closeExtractorDrawer()">
            Close
        </button>
    </div>
    <div class="drawer-content">
        <p>This is where the content for the Extractor will be displayed.</p>
        <p>You can add more specific functionality, forms, or data visualizations here later.</p>
        <p>For example, you might embed another Streamlit component or custom HTML content.</p>
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
    st.session_state.messages.append({"role": "bot", "content": "This is a placeholder response."})
    st.rerun()