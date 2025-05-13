import streamlit as st
import streamlit.components.v1 as components

# --- Session State ---
if "drawer_open" not in st.session_state:
    st.session_state.drawer_open = False
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

# --- Streamlit App Layout ---
st.set_page_config(page_title="ChatBot UI", page_icon="💬", layout="wide")

st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
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
        <p>Args: <span id="argsDisplay"></span></p>
        <button id="testBtn">Send Event to Streamlit</button>
        <script>
            const StreamlitLib = window.parent?.Streamlit;

            function setMinimalHeight() {
                if (StreamlitLib) {
                    StreamlitLib.setFrameHeight(150);
                } else {
                    // console.warn("Minimal: StreamlitLib not found on initial height set.");
                }
            }
            setMinimalHeight(); // Initial call

            const btn = document.getElementById('testBtn');
            if (btn && StreamlitLib) {
                btn.addEventListener('click', () => {
                    StreamlitLib.setComponentValue({ from_minimal_component: "Button Clicked!" });
                });
            } else if (!StreamlitLib) {
                // console.warn("Minimal: StreamlitLib not found for button listener.");
            }


            window.addEventListener("message", event => {
                if (event.data && event.data.type === "streamlit:render") {
                    // console.log("Minimal: Received streamlit:render event", event.detail);
                    if (event.detail && event.detail.args) {
                        document.getElementById('argsDisplay').innerText = JSON.stringify(event.detail.args);
                    }
                    setMinimalHeight(); // Re-set height on render
                }
            });
        </script>
    </body>
    </html>
    """
    
    # Minimal args for testing (if you want to test passing args)
    minimal_args = {"test_arg": "hello from python"}

    component_event = None 
    component_event = components.html(
        minimal_html_content,
        height=150,
        scrolling=False
        # NO key ARGUMENT HERE
        # If you want to pass args, add: args=minimal_args
    )
    st.write("Minimal Component Call Succeeded.")
    if component_event:
        st.write("Event from minimal component:", component_event)

except Exception as e:
    st.error(f"Error during minimal components.html call: {e}")
    st.error(f"Full traceback for minimal error: {type(e).__name__}")

st.write("After Minimal Component Call")