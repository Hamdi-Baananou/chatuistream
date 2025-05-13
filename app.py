import streamlit as st
import streamlit.components.v1 as components

# --- Session State (Keep this for context, though not used in this minimal test directly by component)---
if "drawer_open" not in st.session_state:
    st.session_state.drawer_open = False
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []


# --- Streamlit App Layout ---
st.set_page_config(page_title="ChatBot UI", page_icon="💬", layout="wide")

st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    /* You might not even need these for the minimal test if the component is small */
    /* div[data-testid="stAppViewContainer"] > .main > div[data-testid="block-container"] {
        padding: 0 !important; margin: 0 !important;
        width: 100% !important; 
        max-width: 100% !important; 
    }
    iframe[title^="st.iframe"] {
        border: none !important; 
        width: 100% !important; 
    } */
    body { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)

st.write("Before Minimal Component Call")

try:
    minimal_html_content = """
    <!DOCTYPE html>
    <html>
    <head><title>Minimal Test</title></head>
    <body>
        <h1>Minimal Component Works!</h1>
        <p>Python Args (if any): <span id="argsDisplay"></span></p>
        <button id="testBtn">Send Event to Streamlit</button>
        <script>
            const StreamlitLib = window.parent?.Streamlit; // Optional chaining

            if (StreamlitLib) {
                StreamlitLib.setFrameHeight(150); // Set a fixed small height
            } else {
                console.error("Minimal: StreamlitLib not found");
            }

            const btn = document.getElementById('testBtn');
            if (btn && StreamlitLib) {
                btn.addEventListener('click', () => {
                    StreamlitLib.setComponentValue({ from_minimal_component: "Button Clicked!" });
                });
            }

            // Display args if received
            window.addEventListener("message", event => {
                if (event.data && event.data.type === "streamlit:render") {
                    if (event.detail && event.detail.args) {
                        document.getElementById('argsDisplay').innerText = JSON.stringify(event.detail.args);
                    }
                    if (StreamlitLib) StreamlitLib.setFrameHeight(150);
                }
            });
        </script>
    </body>
    </html>
    """
    
    # Minimal args for testing
    minimal_args = {"test_arg": "hello from python"}

    # Ensure component_event is always defined
    component_event = None 
    component_event = components.html(
        minimal_html_content,
        height=150, # Fixed height for simplicity
        scrolling=False,
        key="minimal_test_component"
        # Removed args for now to simplify, will add back if this works
    )
    st.write("Minimal Component Call Succeeded.")
    if component_event:
        st.write("Event from minimal component:", component_event)

except Exception as e:
    st.error(f"Error during minimal components.html call: {e}")
    st.error(f"Full traceback for minimal error: {type(e).__name__}") # This will show TypeError if that's what it is

st.write("After Minimal Component Call")


# --- Original Event Handling Logic (Commented out for minimal test) ---
# if component_event:
#     action = component_event.get("action")
#     if action == "open_drawer" and not st.session_state.drawer_open:
#         st.session_state.drawer_open = True
#         st.rerun()
#     elif action == "close_drawer" and st.session_state.drawer_open:
#         st.session_state.drawer_open = False
#         st.rerun()

# --- Chat Interface (Commented out for minimal test) ---
# if not st.session_state.drawer_open:
#     st.markdown("<div style='padding: 0 1rem;'>", unsafe_allow_html=True)
#     if not st.session_state.chat_messages:
#         st.info("Welcome! Ask me anything.")
#     # ... rest of chat interface ...
#     st.markdown("</div>", unsafe_allow_html=True)