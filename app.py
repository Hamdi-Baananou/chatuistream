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
        /* background-color: lightblue; */ /* For debugging iframe boundaries */
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
        height: calc(100vh - 60px); /* Fills space below navbar */
        background-color: #f8f9fa;
        z-index: 90; 
        box-shadow: 0 -3px 10px rgba(0,0,0,0.15);
        transform: translateY(calc(100vh - 60px)); /* Start offscreen, considering navbar */
        transition: transform 0.3s ease-in-out;
        padding: 20px; box-sizing: border-box; overflow-y: auto;
        color: #333;
    }}
    .bottom-drawer.open {{ 
        transform: translateY(0); /* Slides up to fill space below navbar */
    }}
    
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
    <div class="container">
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
                <p>More content here to test scrolling...</p>
                {'<p>Paragraph</p>' * 30}
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
        
        // This function is called by Streamlit when the component is rendered or re-rendered
        function onRender(event) {{
            // The first render event might not have event.detail or event.detail.args
            // The initial state (class and height) is handled by the HTML and the script block below.
            if (!event.detail || !event.detail.args) {{
                console.log("iframe: onRender called without args, possibly initial empty render or non-streamlit event.");
                // Ensure height is set on first true render from Streamlit if initial block didn't catch it.
                // This is a fallback. The primary height setting is in the initial script block and args handling.
                if (Streamlit) {{
                    const drawerIsOpen = document.getElementById('bottomDrawerInFrame').classList.contains('open');
                    if (drawerIsOpen) {{
                        Streamlit.setFrameHeight(window.screen.availHeight); 
                    }} else {{
                        Streamlit.setFrameHeight(60); 
                    }}
                }}
                return;
            }}
            
            const args = event.detail.args;
            const drawer = document.getElementById('bottomDrawerInFrame');

            console.log("iframe: onRender received args:", args);

            if (args.drawer_should_be_open) {{
                drawer.classList.add('open');
            }} else {{
                drawer.classList.remove('open');
            }}
            
            if (Streamlit) {{
                if (args.drawer_should_be_open) {{
                    // When drawer is open, the iframe should take full available screen height
                    // to act as an overlay.
                    Streamlit.setFrameHeight(window.screen.availHeight); 
                    console.log("iframe: Set height to full screen:", window.screen.availHeight);
                }} else {{
                    // When drawer is closed, iframe is just the navbar.
                    Streamlit.setFrameHeight(60); 
                    console.log("iframe: Set height to navbar (60px)");
                }}
            }}
        }}

        // Listen for Streamlit's render event
        window.addEventListener("message", event => {{
            if (event.data && event.data.type === "streamlit:render") {{
                onRender(event);
            }}
        }});
        
        // Initial setup: This block runs once when the iframe loads.
        // It sets the initial height based on the `initial_drawer_class`
        // which was determined by Python's session_state.
        // This is important because the first `streamlit:render` event might be delayed
        // or might not contain args immediately.
        (function() {{
            if (Streamlit) {{
                const drawerElement = document.getElementById('bottomDrawerInFrame');
                const initialDrawerIsOpen = drawerElement.classList.contains('open');
                
                console.log("iframe: Initial JS load. Drawer is initially open:", initialDrawerIsOpen);

                if (initialDrawerIsOpen) {{
                    Streamlit.setFrameHeight(window.screen.availHeight);
                    console.log("iframe: Initial height set to full screen:", window.screen.availHeight);
                }} else {{
                    Streamlit.setFrameHeight(60); // Navbar height
                    console.log("iframe: Initial height set to navbar (60px)");
                }}
                // Request args from Streamlit for the first proper onRender call.
                // This ensures that onRender is called with the latest state from Streamlit
                // after the iframe has loaded. Streamlit usually sends one automatically,
                // but this can ensure it if there are timing issues.
                // Streamlit.setComponentReady(); // Not strictly needed if Streamlit.setFrameHeight triggers render
            }} else {{
                console.error("iframe: Streamlit object not available on initial load for height setting.");
                // Fallback if Streamlit object is slow to initialize
                // Attempt to set height after a short delay.
                setTimeout(() => {{
                    if (Streamlit) {{
                        const drawerElement = document.getElementById('bottomDrawerInFrame');
                        const initialDrawerIsOpen = drawerElement.classList.contains('open');
                        if (initialDrawerIsOpen) {{ Streamlit.setFrameHeight(window.screen.availHeight); }}
                        else {{ Streamlit.setFrameHeight(60); }}
                        console.log("iframe: Delayed initial height set. Drawer open:", initialDrawerIsOpen);
                    }} else {{
                        console.error("iframe: Streamlit object still not available after delay.");
                    }}
                }}, 100);
            }}
        }})();
    </script>
</body>
</html>
"""

# --- Streamlit App Layout ---
st.set_page_config(page_title="ChatBot UI", page_icon="💬", layout="wide")

# Custom CSS to remove Streamlit's default header and padding for full-width component
st.markdown("""
<style>
    /* Hide Streamlit's default header */
    header[data-testid="stHeader"] { display: none !important; } 
    
    /* Remove padding from the main block container that holds the iframe */
    div[data-testid="stAppViewContainer"] > .main > div[data-testid="block-container"] {
        padding: 0 !important; 
        margin: 0 !important;
        width: 100% !important;
        max-width: 100% !important; 
    }
    
    /* Ensure iframe itself takes full width and has no border */
    iframe[title^="st.iframe"] {
        border: none !important; 
        width: 100% !important;
        display: block; /* Ensures it behaves like a block element */
        /* Height is managed by Streamlit.setFrameHeight from within the iframe */
    }
    
    /* Ensure body has no margin if not already handled by Streamlit's base CSS */
    body { 
        margin: 0 !important; 
    }

    /* Styling for the chat interface area when visible */
    .chat-container {
        padding: 1rem; /* Horizontal padding for chat messages */
        /* No explicit top padding needed if iframe height is managed correctly */
        /* The chat interface will naturally flow below the 60px iframe component */
        height: calc(100vh - 60px); /* Full remaining height */
        overflow-y: auto; /* Allow chat to scroll */
        box-sizing: border-box;
    }
</style>
""", unsafe_allow_html=True)

# Arguments to pass to the iframe. This ensures the iframe knows the desired drawer state.
component_args = {"drawer_should_be_open": st.session_state.drawer_open}

# The `height` argument here is an initial suggestion.
# The JavaScript inside custom_ui_html will call Streamlit.setFrameHeight
# to dynamically adjust the iframe's height based on drawer state.
# Starting with 60px is safe for the navbar-only state. If the drawer
# is meant to be open initially, the JS will quickly expand it.
component_event = components.html(
    custom_ui_html,
    height=60, # Initial height, JS will adjust.
    scrolling=False,
    key="custom_navbar_drawer_ui" # Removed args parameter as it's not used by components.html
                                 # Args are typically passed via Streamlit.setComponentValue or initial render
)
# The `component_args` dictionary is not directly passed to `components.html` like that.
# Streamlit sends these arguments to the component's `onRender` function automatically
# when the component is (re)rendered due to a Streamlit rerun if those args change the key
# or if we explicitly use `st.experimental_rerun(args=...)` or similar mechanisms.
# For this setup, the `component_args` are implicitly available in the `onRender` function
# as `event.detail.args` when Streamlit re-renders the component due to `st.rerun()`.

# Handle events sent from the iframe
if component_event:
    action = component_event.get("action")
    if action == "open_drawer" and not st.session_state.drawer_open:
        st.session_state.drawer_open = True
        st.rerun()
    elif action == "close_drawer" and st.session_state.drawer_open:
        st.session_state.drawer_open = False
        st.rerun()

# --- Chat Interface ---
# This will appear below the 60px iframe component when the drawer is closed.
if not st.session_state.drawer_open:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

    if not st.session_state.chat_messages:
        st.info("Welcome! Ask me anything about LEONI. The Extractor is available via the ✨ button.")

    for msg_idx, msg in enumerate(st.session_state.chat_messages):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_prompt = st.chat_input("Your message...", key="main_chat_input")

    if user_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        # Simulate bot response
        st.session_state.chat_messages.append({"role": "assistant", "content": f"Echo from bot: {user_prompt}"})
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)