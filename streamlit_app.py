
import streamlit as st

from src.assistant import create_assistant
from src.memory import create_memory


st.set_page_config(
    page_title="AI Personal Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI Personal Assistant")
st.caption("Powered by LangChain tool calling")

# Initialize the assistant once per browser session.
if "chat" not in st.session_state:
    memory = create_memory()
    st.session_state.chat = create_assistant(memory)
    st.session_state.messages = []

# Display previous messages.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept a new message.
if prompt := st.chat_input("Ask me to manage tasks, meetings, or orders..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking and executing tools..."):
            try:
                reply = st.session_state.chat(prompt)
            except Exception:
                reply = (
                    "Sorry, something went wrong. "
                    "Please check the application configuration."
                )

        st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )
