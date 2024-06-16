import os
from typing import Type

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1
from dotenv import load_dotenv
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS  # vector store
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint import MemorySaver  # an in-memory checkpointer
from langgraph.prebuilt import create_react_agent

load_dotenv()

st.set_page_config(layout="wide")


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
if "col1_result" not in st.session_state:
    st.session_state.col1_result = ""

if "col2_result" not in st.session_state:
    st.session_state.col2_result = ""


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


url_list = ["https://github.com/trending", "https://github.com/trending/developers"]

docs = []
for path in url_list:
    loader = WebBaseLoader(web_paths=(path,))
    docs += loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(documents=splits, embedding=OpenAIEmbeddings())
retriever = vectorstore.as_retriever()


tool = create_retriever_tool(
    retriever,
    "github_trending_repositories_and_developers_retriever",
    "Searches and returns trending repositories and developers on github "
    "that are similar to the given query",
)

llm = ChatOpenAI(model="gpt-4o")
tools = [GithubActivityTool(), tool]


system_message = "You are a helpful assistant."

memory = MemorySaver()
app = create_react_agent(
    llm, tools, messages_modifier=system_message, checkpointer=memory
)

config = {"configurable": {"thread_id": "test-thread"}}

st.title("Demo UI")

destinations = [
    {"name": "Shirogane Blue Pond", "latitude": 43.551, "longitude": 142.686},
    {"name": "Otaru Aquarium", "latitude": 43.202, "longitude": 140.998},
    {
        "name": "Nikka Whisky Yoichi Distillery",
        "latitude": 43.197,
        "longitude": 140.774,
    },
    {"name": "Ainu Museum (Upopoy)", "latitude": 42.556, "longitude": 141.360},
    {"name": "Unkai Terrace", "latitude": 43.069, "longitude": 142.634},
]

# Create a DataFrame
df = pd.DataFrame(destinations)

st.data_editor(df, num_rows="dynamic")

path_to_html = "/workspaces/Transcendent/notebooks/hokkaido_map.html"

with open(path_to_html, "r") as f:
    html_data = f.read()

# Show in webpage
st.header("Show an external HTML")
st.components.v1.html(html_data, scrolling=True, height=500)

col1, col2 = st.columns(2)

with col1:
    with st.container():
        st.write("Sample placeholder Github Events Feed:")

        if st.button("Click me to fetch Github Events Feed"):
            with st.spinner("Agent is fetching and summarizing the data..."):
                message = (
                    "user",
                    f"whanyu1212, {GITHUB_ACCESS_TOKEN}. Return the summarized text as "
                    "well as the frequency table of different types of events.",
                )
                st.session_state.col1_result = app.invoke(
                    {"messages": [message]}, config
                )["messages"][-1].content

        st.markdown(st.session_state.col1_result)

with col2:
    with st.container():
        st.write("Sample placeholder Github Trending Repo:")

        if st.button(
            "Click me to fetch Trending repositories related to "
            "machine learning, AI and data science"
        ):
            with st.spinner("Agent is fetching and summarizing the data..."):
                message = (
                    "user",
                    "What are the trending repositories that are related to "
                    "machine learning, AI, and data science today?",
                )
                st.session_state.col2_result = app.invoke(
                    {"messages": [message]}, config
                )["messages"][-1].content

        st.markdown(st.session_state.col2_result)
