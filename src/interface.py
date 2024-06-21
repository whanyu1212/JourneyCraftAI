import os
import time

import joblib
import streamlit as st
from langchain_google_vertexai import ChatVertexAI  # noqa: F401
from streamlit_lottie import st_lottie  # noqa: F401

st.set_page_config(
    layout="wide",
)


st.lottie(
    "https://lottie.host/5d26fdfc-db1d-4533-a143-4139bb57124c/DUfq4gKFIa.json",
    height=200,
    width=200,
)

st.title("JourneyCraftAI")
new_chat_id = f"{time.time()}"

# Create a directory to store the chat history of the user
try:
    os.mkdir("data/")
except FileExistsError:
    pass


try:
    past_chats: dict = joblib.load("data/past_chats_list")
except FileNotFoundError:
    past_chats = {}


with st.sidebar:
    st.markdown("## Past Conversations")
    st.divider()

    if st.session_state.get("chat_id") is None:
        st.session_state.chat_id = st.selectbox(
            label="Pick a past chat",
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, "New Chat"),
            placeholder="_",
        )
    else:
        # This will happen the first time AI response comes in
        st.session_state.chat_id = st.selectbox(
            label="Pick a past chat to revisit",
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(
                x,
                (
                    "New Chat"
                    if x != st.session_state.chat_id
                    else st.session_state.chat_title
                ),
            ),
            placeholder="_",
        )
    # TODO: Use llm to summarize the chat and give a chat title
    st.session_state.chat_title = f"ChatSession-{st.session_state.chat_id}"


with st.expander(":exclamation: Disclaimer"):
    st.write(
        """
    Agent can be slow to respond because it is executing tasks in the background.
    It can also make mistakes and may not be able to answer all questions.
    """
    )
