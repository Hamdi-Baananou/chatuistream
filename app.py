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
custom_ui_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
    body {{ margin: 0; font-family: 'Arial', sans-serif; overflow: hidden; /* Prevent body scroll, iframe handles it */ }}
    .container {{ 
        /* This container will hold the navbar and the drawer */
        /* It needs to allow the drawer to overlay correctly */
        position: relative; 
        width: 100vw; 
        height: 100vh; 
    }}
    .navbar {{
        position: fixed; /* Fixed within the iframe */
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
        position: fixed; /* Fixed within the iframe */
        bottom: 0; left: 0; right: 0; 
        width: 100%;
        height: calc(100vh - 60px); /* Fills space below navbar */
        background-color: #f8f9fa;
        z-index: 90; /* Below navbar, above other potential iframe content */
        box-shadow: 0 -3px 10px rgba(0,0,0,0.15);
        transform: translateY(100%); /* Start off-screen (slid down fully) */
        transition: transform 0.3s ease-in-out;
        padding: 20px; box-sizing: border-box; overflow-y: auto;
        color: #333;
    }}
    .bottom-drawer.open {{ transform: translateY(0); }} /* Slide into view */
    
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
    <div class="container"> {/* Main container for iframe content */}
        <div class="navbar">
            <div class="company-name">LEONI</div>
            <button id="extractorBtnInFrame" class="extractor-button">
                ✨ Extractor
            </button>
        </div>

        <div id="bottomDrawerInFrame" class="bottom-drawer"> {/* Drawer content */}
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
        // Ensure Streamlit communication object is available from the parent window
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
        
        // Function to handle render events from Streamlit (e.g., when args change)
        function onRender(event) {{
            if (!event.detail || !event.detail.args) {{
                // console.log("iframe: onRender called without args or detail");
                if (Streamlit) Streamlit.setFrameHeight(window.innerHeight); // Set to full height
                return;
            }}
            
            const args = event.detail.args;
            const drawer = document.getElementById('bottomDrawerInFrame');

            // console.log("iframe: onRender received args:", args);

            if (args.drawer_should_be_open) {{
                drawer.classList.add('open');
            }} else {{
                drawer.classList.remove('open');
            }}
            
            // The component should take full viewport height because it manages its own overlay
            if (Streamlit) {{
                Streamlit.setFrameHeight(window.innerHeight); 
            }}
        }}

        // Listen for messages from Streamlit parent
        window.addEventListener("message", event => {{
            // A more secure check for origin might be needed if deploying publicly
            // if (event.origin !== window.location.ancestorOrigins[0]) return; 
            if (event.data && event.data.type === "streamlit:render") {{
                onRender(event);
            }}
        }});
        
        // Initial setup: tell Streamlit the component is ready and its desired height
        // This might also be triggered by the first "streamlit:render" event.
        if (Streamlit) {{
            Streamlit.setFrameHeight(window.innerHeight); // Tell parent to make iframe full height
            // Send an initial "ready" or request initial state if needed
            // Streamlit.setComponentValue({status: "iframe_ready"});
        }} else {{
            console.error("iframe: Streamlit object not available on initial load.");
        }}
    </script>
</body>
</html>
"""

# --- Streamlit App Layout ---
st.set_page_config(page_title="ChatBot UI", page_icon="💬", layout="wide")

# CSS to make the iframe take full width and remove Streamlit's default header/padding
st.markdown("""
<style>
    /* Remove Streamlit's default header */
    header[data-testid="stHeader"] { display: none !important; }
    
    /* Ensure the block container and app view container for the component take full width/height */
    /* And remove padding around the component itself */
    div[data-testid="stAppViewContainer"] > .main > div[data-testid="block-container"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    iframe[title^="st.iframe"] { /* Selects iframes created by st.components.v1.html */
        border: none !important; /* Remove iframe border */
        width: 100vw !important;
        height: 100vh !important; /* Make iframe take full viewport height */
    }
    /* Ensure no body margin in the main Streamlit app if it affects layout */
    body { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

# Arguments to pass to the HTML component
component_args = {"drawer_should_be_open": st.session_state.drawer_open}

# Embed the custom UI as an HTML component
# The component will take full screen. The chat will be "behind" it conceptually.
# If you want chat visible simultaneously, this design needs changing.
component_event = components.html(
    custom_ui_html,
    height=0, # Initial height, JS in iframe will call Streamlit.setFrameHeight(window.innerHeight)
    scrolling=False, # The iframe itself shouldn't scroll; content inside it can.
    key="custom_navbar_drawer_ui" # Unique key
)

# Handle actions sent from the HTML component
if component_event:
    action = component_event.get("action")
    # print(f"Streamlit: Received action from component: {action}") # For debugging
    if action == "open_drawer" and not st.session_state.drawer_open:
        st.session_state.drawer_open = True
        st.rerun() # Rerun to update component_args and re-render component
    elif action == "close_drawer" and st.session_state.drawer_open:
        st.session_state.drawer_open = False
        st.rerun()

# --- Chat Interface ---
# Since the component above takes 100vh, this chat interface might be
# visually "underneath" or not accessible unless the component's height
# is managed differently (e.g., only 60px when drawer is closed).

# If the component always takes 100vh:
# To have the chat interface, it would need to be *part of the component's HTML*
# or the component's height logic needs to be smarter:
# - 60px height when drawer is closed (to show only navbar)
# - 100vh height when drawer is open (to overlay)
#
# For the current `custom_ui_html` which sets iframe height to `window.innerHeight`,
# the following Streamlit chat elements will be rendered but likely not visible.
# Let's comment it out for now to focus on the component.

"""
# Add some space if the navbar is only 60px from the component
# st.markdown("<div style='padding-top: 70px;'></div>", unsafe_allow_html=True)

# Welcome message and chat display
# if not st.session_state.chat_messages:
#     st.info("Welcome! Ask me anything.")

# for msg_idx, msg in enumerate(st.session_state.chat_messages):
#     with st.chat_message(msg["role"], avatar="🧑‍💻" if msg["role"] == "user" else "🤖"):
#         st.write(msg["content"])

# user_prompt = st.chat_input("Your message...", key="main_chat_input")

# if user_prompt:
#     st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
#     # Simulate bot response
#     st.session_state.chat_messages.append({"role": "assistant", "content": f"Echo: {user_prompt}"})
#     st.rerun() # Rerun to display new messages
"""