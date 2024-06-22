import os
import time

import autogen  # noqa: F401
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components  # noqa: F401
from autogen.coding import LocalCommandLineCodeExecutor  # noqa: F401
from langchain_google_vertexai import ChatVertexAI  # noqa: F401
from streamlit_lottie import st_lottie  # noqa: F401

from trip_agents import TripAgents  # noqa: F401

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


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/workspaces/JourneyCraftAI/fleet-anagram-244304-b19fa2de9084.json"
)

llm = ChatVertexAI(model="gemini-1.5-pro")


with st.sidebar:
    st.markdown("## Past Conversations")
    st.divider()


with st.expander(":exclamation: Disclaimer", expanded=True):
    st.markdown(
        """
    <style>
    .info {color: grey;}
    </style>
    <p class="info">
    Agent can be slow to respond because it is executing tasks in the background.
    It can also make mistakes and may not be able to answer all questions.
    </p>
    """,
        unsafe_allow_html=True,
    )

# session states
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("The Agent is thinking..."):
            message_placeholder = st.empty()
            # full_response = llm.invoke(prompt)
            # message_placeholder.markdown(full_response.content)
            trip_agents = TripAgents()
            full_response = trip_agents.user_proxy.initiate_chat(
                trip_agents.assistant,
                message=prompt,
                summary_method="reflection_with_llm",
            )
            if "itinerary.csv" in os.listdir("coding"):
                df = pd.read_csv("./coding/itinerary.csv")

    st.data_editor(df, use_container_width=True)
    st.text("")
    path_to_html = "./coding/map.html"

    with open(path_to_html, "r") as f:
        html_data = f.read()
    st.components.v1.html(html_data, scrolling=True, height=500)
    # message_placeholder.markdown(df)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
