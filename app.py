import streamlit as st
# Removed unused imports: streamlit_extras.colored_header, streamlit.components.v1

# Page configuration
st.set_page_config(
    page_title="ChatBot UI",
    page_icon="💬",
    layout="wide"
)

# Initialize session state for drawer
if "drawer_open" not in st.session_state:
    st.session_state.drawer_open = False

# --- Query Parameter Handling ---
# This logic processes the action from the URL.
# It changes session state and triggers a rerun if the state needs to change.
# It's designed to not loop if the URL param matches the current state.
if "drawer_action" in st.query_params:
    action = st.query_params.get("drawer_action")
    
    drawer_is_currently_open = st.session_state.get("drawer_open", False)
    action_caused_state_change = False

    if action == "open" and not drawer_is_currently_open:
        st.session_state.drawer_open = True
        action_caused_state_change = True
    elif action == "close" and drawer_is_currently_open:
        st.session_state.drawer_open = False
        action_caused_state_change = True
    
    if action_caused_state_change:
        # We need to remove the query param from the URL to prevent it from
        # being reprocessed on subsequent non-action reruns or if the user bookmarks/reloads.
        # The cleanest way is to navigate. However, Streamlit doesn't have a direct
        # "redirect to new URL without param" Python command that doesn't involve JS.
        # The current JS already handles navigation. The st.rerun() ensures the Python UI updates.
        st.rerun()

# --- HTML, CSS, and JavaScript Injection ---
# Determine drawer class based on session state
drawer_visibility_class = "open" if st.session_state.get("drawer_open", False) else ""

html_content = f"""
<style>
    /* Main container padding */
    body {{ margin: 0; }} /* Reset body margin for consistency */
    .main {{ padding: 0rem 1rem; }}
    
    /* Navbar styling */
    .navbar {{
        position: fixed; top: 0; left: 0; right: 0; background-color: #ffffff;
        padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        z-index: 9999; display: flex; justify-content: space-between;
        align-items: center; height: 60px; box-sizing: border-box;
    }}
    .company-name {{
        font-size: 1.8rem; font-weight: 700; color: #1E1E1E; text-decoration: none;
        font-family: 'Arial', sans-serif; letter-spacing: 1px;
    }}
    /* Custom button styling for navbar */
    .extractor-button {{
        background-color: #4CAF50; color: white; padding: 0.5rem 1.5rem;
        border-radius: 20px; border: none; font-weight: 500; cursor: pointer;
        transition: background-color 0.3s ease; font-size: 1rem;
        display: inline-flex; align-items: center; gap: 0.5em;           
    }}
    .extractor-button:hover {{ background-color: #45a049; }}
    
    /* Streamlit's default header (if visible) */
    .stApp > header {{ display: none !important; }} /* Hide Streamlit's default header */
    
    /* Chat input styling */
    .stTextInput > div > div > input {{ border-radius: 20px; padding: 10px 20px; }}
    
    /* Chat message styling */
    .chat-message {{
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem;
        display: flex; flex-direction: column;
    }}
    .chat-message.user {{ background-color: #2b313e; }}
    .chat-message.bot {{ background-color: #475063; }}
    .chat-message .message {{ width: 100%; padding: 0; }}
    
    /* Main content padding to account for fixed navbar */
    /* Target Streamlit's main view container more reliably */
    div[data-testid="stAppViewContainer"] > section {{
        padding-top: 75px !important; /* 60px navbar + 15px buffer */
    }}
    
    /* Ensure main app content z-index is low */
    .stApp > main {{ z-index: 1; }}

    /* Bottom Drawer Styling */
    .bottom-drawer {{
        position: fixed; bottom: 0; left: 0; right: 0; width: 100%;
        height: calc(100vh - 60px); background-color: #f8f9fa;
        z-index: 9990; box-shadow: 0 -3px 10px rgba(0,0,0,0.15);
        transform: translateY(100%); transition: transform 0.3s ease-in-out;
        padding: 20px; box-sizing: border-box; overflow-y: auto;
    }}
    .bottom-drawer.open {{ transform: translateY(0); }}
    .drawer-header {{
        display: flex; justify-content: space-between; align-items: center;
        padding-bottom: 15px; border-bottom: 1px solid #e0e0e0; margin-bottom: 15px;
    }}
    .drawer-header h2 {{ margin: 0; font-size: 1.5rem; color: #333; }}
    .close-drawer-button {{
        background-color: #e74c3c; color: white; padding: 0.4rem 1rem; border: none;
        border-radius: 15px; font-weight: 500; cursor: pointer;
        transition: background-color 0.3s ease; font-size: 0.9rem;
    }}
    .close-drawer-button:hover {{ background-color: #c0392b; }}
    .drawer-content {{ color: #333; }}
</style>

<!-- Navbar HTML (NO INLINE ONCLICK) -->
<div class="navbar">
    <div class="company-name">LEONI</div>
    <button id="extractorBtn" class="extractor-button">
        ✨ Extractor
    </button>
</div>

<!-- Drawer HTML (NO INLINE ONCLICK) -->
<div id="bottomDrawer" class="bottom-drawer {drawer_visibility_class}">
    <div class="drawer-header">
        <h2>Extractor Details</h2>
        <button id="closeDrawerBtn" class="close-drawer-button">
            Close
        </button>
    </div>
    <div class="drawer-content">
        <p>This is where the content for the Extractor will be displayed.</p>
        <p>You can add more specific functionality, forms, or data visualizations here later.</p>
    </div>
</div>

<script>
    // Define actions
    function triggerDrawerAction(actionType) {{
        const currentUrl = new URL(window.location.href);
        currentUrl.searchParams.set('drawer_action', actionType);
        // Remove the param if it's already set to the same action to avoid no-op navigation if possible,
        // though navigating to the same URL with same params is usually fine.
        // Or ensure the Python side handles no-op gracefully.
        window.location.href = currentUrl.toString();
    }}

    // Attach event listeners
    // We need to ensure this script runs after elements are in DOM.
    // For st.markdown, the script at the end of the block should be fine.
    // To be robust against multiple executions of this script block if Streamlit
    // were to re-render it without a full page reload (less common for st.markdown):
    
    const extractorButton = document.getElementById('extractorBtn');
    if (extractorButton && !extractorButton.hasAttribute('data-listener-attached')) {{
        extractorButton.addEventListener('click', function() {{ triggerDrawerAction('open'); }});
        extractorButton.setAttribute('data-listener-attached', 'true');
    }}

    const closeButton = document.getElementById('closeDrawerBtn');
    if (closeButton && !closeButton.hasAttribute('data-listener-attached')) {{
        closeButton.addEventListener('click', function() {{ triggerDrawerAction('close'); }});
        closeButton.setAttribute('data-listener-attached', 'true');
    }}
</script>
"""
st.markdown(html_content, unsafe_allow_html=True)


# --- MAIN CHAT INTERFACE (Below the fixed elements) ---
# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0;'>
        <h1>Welcome to the ChatBot</h1>
        <p>How can I help you today?</p>
    </div>
    """, unsafe_allow_html=True)

# Chat input
user_input = st.text_input("", placeholder="Type your message here...", key="input_main_chat") 

# Display chat messages
for message_idx, message in enumerate(st.session_state.messages):
    with st.container(): # Using key for containers if there are many dynamic ones
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