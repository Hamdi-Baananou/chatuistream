import streamlit as st
import streamlit.components.v1 as components

# --- Session State ---
if "drawer_open" not in st.session_state:
    st.session_state.drawer_open = False
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# --- Component HTML/JS (Content for the iframe) ---
# This HTML will live inside the iframe.
# It communicates with the parent Streamlit app.
# Determine drawer class based on current session state for initial load
initial_drawer_class = "open" if st.session_state.drawer_open else ""

custom_ui_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
    body {{ margin: 0; font-family: 'Arial', sans-serif; overflow: hidden; }}
    .container {{ 
        position: relative; 
        width: 100vw; 
        height: 100vh; 
    }}
    .navbar {{
        position: fixed;
        top: 0; left: 0; right: 0; background-color: #ffffff;
        padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        z-index: 100; display: flex; justify-content: space-between;
        align-items: center; height: 60px; box-sizing: border-box;
    }}
    .company-name {{ font-size: 1.8rem; font-weight: 700; color: #1E1E1E; }}
    .extractor-button {{
        background-color: #4CAF50; color: white; padding: 0.5rem 1.5rem;
        border-radius: 20px; border: none; font-weight: 500; cursor: pointer;
        transition: background-color 0.3s ease; font-size: 1rem;
        display: inline-flex; align-items: center; gap: 0.5em;
    }}
    .extractor-button:hover {{ background-color: #45a049; }}

    .bottom-drawer {{
        position: fixed; 
        bottom: 0; left: 0; right: 0; 
        width: 100%;
        height: calc(100vh - 60px); 
        background-color: #f8f9fa;
        z-index: 90; 
        box-shadow: 0 -3px 10px rgba(0,0,0,0.15);
        transform: translateY(100%); 
        transition: transform 0.3s ease-in-out;
        padding: 20px; box-sizing: border-box; overflow-y: auto;
        color: #333;
    }}
    .bottom-drawer.open {{ transform: translateY(0); }}
    
    .drawer-header {{
        display: flex; justify-content: space-between; align-items: center;
        padding-bottom: 15px; border-bottom: 1px solid #e0e0e0; margin-bottom: 15px;
    }}
    .drawer-header h2 {{ margin: 0; font-size: 1.5rem; }}
    .close-drawer-button {{
        background-color: #e74c3c; color: white; padding: 0.4rem 1rem; border: none;
        border-radius: 15px; font-weight: 500; cursor: pointer;
        transition: background-color 0.3s ease; font-size: 0.9rem;
    }}
    .close-drawer-button:hover {{ background-color: #c0392b; }}
    .drawer-content p {{ color: #333; }}
</style>
</head>
<body>
    <div class="container"> <!-- Main container for iframe content -->
        <div class="navbar">
            <div class="company-name">LEONI</div>
            <button id="extractorBtnInFrame" class="extractor-button">
                ✨ Extractor
            </button>
        </div>

        <!-- Drawer content. Initial class is set by Python f-string -->
        <div id="bottomDrawerInFrame" class="bottom-drawer {initial_drawer_class}"> 
            <div class="drawer-header">
                <h2>Extractor Details</h2>
                <button id="closeDrawerBtnInFrame" class="close-drawer-button">
                    Close
                </button>
            </div>
            <div class="drawer-content">
                <p>This is where the content for the Extractor will be displayed in the iframe.</p>
            </div>
        </div>
    </div>

    <script>
        const Streamlit = window.parent.Streamlit;

        function sendActionToStreamlit(actionType) {{
            if (Streamlit) {{
                Streamlit.setComponentValue({{ action: actionType }});
            }} else {{
                console.error("Streamlit communication object not found in iframe.");
            }}
        }}

        document.getElementById('extractorBtnInFrame').addEventListener('click', function() {{
            sendActionToStreamlit('open_drawer');
        }});

        document.getElementById('closeDrawerBtnInFrame').addEventListener('click', function() {{
            sendActionToStreamlit('close_drawer');
        }});
        
        function onRender(event) {{
            if (!event.detail || !event.detail.args) {{
                if (Streamlit) Streamlit.setFrameHeight(window.innerHeight);
                return;
            }}
            
            const args = event.detail.args;
            const drawer = document.getElementById('bottomDrawerInFrame');

            if (args.drawer_should_be_open) {{
                drawer.classList.add('open');
            }} else {{
                drawer.classList.remove('open');
            }}
            
            // Option 1: Always full height for overlay
            // if (Streamlit) Streamlit.setFrameHeight(window.innerHeight); 

            // Option 2: Adjust height based on drawer state (to show chat below)
            if (Streamlit) {{
                if (args.drawer_should_be_open) {{
                    Streamlit.setFrameHeight(window.innerHeight); // Full height for overlay
                }} else {{
                    Streamlit.setFrameHeight(60); // Only navbar height
                }}
            }}
        }}

        window.addEventListener("message", event => {{
            if (event.data && event.data.type === "streamlit:render") {{
                onRender(event);
            }}
        }});
        
        // Initial render call to set height and drawer state based on initial args
        // Streamlit typically sends an initial render event, but this can help.
        // However, the `onRender` function itself is designed to be called by Streamlit.
        // So, it's better to rely on Streamlit's initial "streamlit:render" message.
        // The `initial_drawer_class` in the HTML helps with the very first paint.
        if (Streamlit) {{
            // Set initial height based on drawer state
            const initialDrawerIsOpen = document.getElementById('bottomDrawerInFrame').classList.contains('open');
            if (initialDrawerIsOpen) {{
                 Streamlit.setFrameHeight(window.innerHeight);
            }} else {{
                 Streamlit.setFrameHeight(60);
            }}
        }} else {{
            console.error("iframe: Streamlit object not available on initial load for height setting.");
        }}
    </script>
</body>
</html>
"""

# --- Streamlit App Layout ---
st.set_page_config(page_title="ChatBot UI", page_icon="💬", layout="wide")

st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stAppViewContainer"] > .main > div[data-testid="block-container"] {
        padding: 0 !important; margin: 0 !important;
        width: 100% !important; /* Ensure block container also takes full width */
        max-width: 100% !important; /* Override Streamlit's max-width if any */
    }
    iframe[title^="st.iframe"] {
        border: none !important; 
        width: 100% !important; /* Changed from 100vw to 100% to be relative to parent */
        /* height is managed by the component itself via Streamlit.setFrameHeight */
    }
    body { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

component_args = {"drawer_should_be_open": st.session_state.drawer_open}

component_event = components.html(
    custom_ui_html,
    height=60 if not st.session_state.drawer_open else 0, # Initial height guess. JS will correct.
    scrolling=False, 
    key="custom_navbar_drawer_ui"
)

if component_event:
    action = component_event.get("action")
    if action == "open_drawer" and not st.session_state.drawer_open:
        st.session_state.drawer_open = True
        st.rerun() 
    elif action == "close_drawer" and st.session_state.drawer_open:
        st.session_state.drawer_open = False
        st.rerun()

# --- Chat Interface ---
# This will now appear below the 60px iframe component when the drawer is closed.
# No extra padding-top div is needed if the component correctly sets its height to 60px.

if not st.session_state.drawer_open: # Only show chat if drawer is closed
    st.markdown("<div style='padding: 0 1rem;'>", unsafe_allow_html=True) # Add some horizontal padding for chat

    if not st.session_state.chat_messages:
        st.info("Welcome! Ask me anything.")

    for msg_idx, msg in enumerate(st.session_state.chat_messages):
        # Using Streamlit's native chat elements for better styling and functionality
        with st.chat_message(msg["role"]): 
            st.write(msg["content"])

    user_prompt = st.chat_input("Your message...", key="main_chat_input")

    if user_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        # Simulate bot response
        st.session_state.chat_messages.append({"role": "assistant", "content": f"Echo from bot: {user_prompt}"})
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)