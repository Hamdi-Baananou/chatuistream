# (Keep the Python code before this as is)

# --- Component HTML/JS (Content for the iframe) ---
initial_drawer_class = "open" if st.session_state.drawer_open else ""
# Convert Python boolean to JavaScript boolean string
js_initial_drawer_state = "true" if st.session_state.drawer_open else "false"


custom_ui_html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
    {'''/* ... all your CSS rules ... */'''}
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
        // Correctly initialize currentDrawerState using the Python-generated JS boolean string
        let currentDrawerState = {js_initial_drawer_state}; // Initialize from Python

        // Ensure Streamlit communication object is available
        let Streamlit = window.parent ? window.parent.Streamlit : null;

        function sendActionToStreamlit(actionType) {{
            if (Streamlit) {{
                Streamlit.setComponentValue({{ action: actionType }});
            }} else {{
                console.error("Streamlit communication object not found in iframe for sendAction.");
                // Fallback or re-check for Streamlit object
                if (window.parent && window.parent.Streamlit) Streamlit = window.parent.Streamlit;
            }}
        }}

        document.getElementById('extractorBtnInFrame').addEventListener('click', function() {{
            sendActionToStreamlit('open_drawer');
        }});

        document.getElementById('closeDrawerBtnInFrame').addEventListener('click', function() {{
            sendActionToStreamlit('close_drawer');
        }});
        
        function setFrameHeightBasedOnDrawerState(isDrawerOpen) {{
            if (Streamlit) {{
                if (isDrawerOpen) {{
                    Streamlit.setFrameHeight(window.innerHeight); 
                }} else {{
                    Streamlit.setFrameHeight(60); 
                }}
            }} else {{
                 console.error("Streamlit communication object not found for setFrameHeight.");
                 if (window.parent && window.parent.Streamlit) Streamlit = window.parent.Streamlit;
            }}
        }}

        function onRender(event) {{
            if (!Streamlit && window.parent && window.parent.Streamlit) {{
                Streamlit = window.parent.Streamlit;
            }}

            if (!event || !event.detail || !event.detail.args) {{
                // console.log("iframe: onRender called without args. Setting height based on current JS state: " + currentDrawerState);
                setFrameHeightBasedOnDrawerState(currentDrawerState);
                return;
            }}
            
            const args = event.detail.args;
            const drawer = document.getElementById('bottomDrawerInFrame');
            const newDrawerStateFromArgs = args.drawer_should_be_open;

            // console.log("iframe: onRender received args:", args, "New state from args:", newDrawerStateFromArgs);

            if (newDrawerStateFromArgs) {{
                drawer.classList.add('open');
            }} else {{
                drawer.classList.remove('open');
            }}
            currentDrawerState = newDrawerStateFromArgs; // Update local JS state
            setFrameHeightBasedOnDrawerState(newDrawerStateFromArgs);
        }}

        window.addEventListener("message", event => {{
            if (event.data && event.data.type === "streamlit:render") {{
                onRender(event);
            }}
        }});
        
        // Attempt initial height setting.
        // This will use the `currentDrawerState` initialized from Python via `js_initial_drawer_state`.
        // A small delay can help ensure the Streamlit object has a chance to be there.
        setTimeout(() => {{
            if (!Streamlit && window.parent && window.parent.Streamlit) {{
                Streamlit = window.parent.Streamlit;
            }}
            // console.log("iframe: Attempting initial height setting. Current JS drawer state: " + currentDrawerState);
            setFrameHeightBasedOnDrawerState(currentDrawerState);
        }}, 50); // 50ms delay, adjust if needed

    </script>
</body>
</html>
"""

# (Keep the Python code after this, like st.set_page_config, st.markdown for global styles, 
#  components.html call, event handling, and chat interface, as is from the previous version)
# --- Streamlit App Layout ---
st.set_page_config(page_title="ChatBot UI", page_icon="💬", layout="wide")

st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stAppViewContainer"] > .main > div[data-testid="block-container"] {
        padding: 0 !important; margin: 0 !important;
        width: 100% !important; 
        max-width: 100% !important; 
    }
    iframe[title^="st.iframe"] {
        border: none !important; 
        width: 100% !important; 
    }
    body { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

# Args are not strictly needed by components.html itself for its own rendering,
# but are passed to the iframe's `onRender` event.
component_args = {"drawer_should_be_open": st.session_state.drawer_open}

component_event = components.html(
    custom_ui_html,
    height=60, # Start with a fixed small height. JS will adjust.
    scrolling=False,
    key="custom_navbar_drawer_ui" # Unique key
)

if component_event:
    action = component_event.get("action")
    # print(f"Streamlit App: Received action '{action}'") # Debugging
    if action == "open_drawer" and not st.session_state.drawer_open:
        st.session_state.drawer_open = True
        # print(f"Streamlit App: Set drawer_open to True. Rerunning.") # Debugging
        st.rerun()
    elif action == "close_drawer" and st.session_state.drawer_open:
        st.session_state.drawer_open = False
        # print(f"Streamlit App: Set drawer_open to False. Rerunning.") # Debugging
        st.rerun()

# --- Chat Interface ---
if not st.session_state.drawer_open:
    st.markdown("<div style='padding: 0 1rem;'>", unsafe_allow_html=True)

    if not st.session_state.chat_messages:
        st.info("Welcome! Ask me anything.")

    for msg_idx, msg in enumerate(st.session_state.chat_messages):
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_prompt = st.chat_input("Your message...", key="main_chat_input")

    if user_prompt:
        st.session_state.chat_messages.append({"role": "user", "content": user_prompt})
        st.session_state.chat_messages.append({"role": "assistant", "content": f"Echo from bot: {user_prompt}"})
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)