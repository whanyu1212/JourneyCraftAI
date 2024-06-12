import os
from typing import Type

import requests
import streamlit as st
from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_openai import (  # tend to use this whenever gemini runs into quota limit
    ChatOpenAI,
)
from langgraph.checkpoint import MemorySaver  # an in-memory checkpointer
from langgraph.prebuilt import create_react_agent

load_dotenv()


# For tracing and debugging
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
#     "/workspaces/Transcendent/fleet-anagram-244304-7dafcc771b2f.json"
# )

# if you are using text embedding model from google
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Let's define a custom tool by subclassing the BaseTool class (from langchain)


class GithubUserCredentials(BaseModel):
    username: str = Field(description="Github username")
    github_access_token: str = Field(description="Github access token")


class GithubActivityTool(BaseTool):
    name = "Github_Activity_Tool"
    description = "useful for when you need to track user's github activity / events"
    args_schema: Type[BaseModel] = GithubUserCredentials

    def _run(self, username, github_access_token):
        url = f"https://api.github.com/users/{username}/events"
        headers = {"Authorization": f"token {github_access_token}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        events_data = response.json()
        return events_data


llm = ChatOpenAI(model="gpt-4o")
tools = [GithubActivityTool()]


system_message = "You are a helpful assistant."

memory = MemorySaver()
app = create_react_agent(
    llm, tools, messages_modifier=system_message, checkpointer=memory
)

config = {"configurable": {"thread_id": "test-thread"}}

st.title("Demo UI")

with st.container():
    st.write("Sample placeholder Github Events Feed:")

    if st.button("Click me to fetch Github Events Feed"):
        with st.spinner("Agent is fetching and summarizing the data..."):
            message = (
                "user",
                f"whanyu1212, {GITHUB_ACCESS_TOKEN}. Return the summarized text as "
                "well as the frequency table of different types of events.",
            )
            result = app.invoke({"messages": [message]}, config)["messages"][-1].content
            st.markdown(result)
