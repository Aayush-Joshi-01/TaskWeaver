# Import necessary libraries
import os
import re
import sys
import pandas as pd
import streamlit as st
from typing import Any, Dict, List, Optional, Tuple
import requests

# Initialize Streamlit app
st.title("TaskWeaver App")

# Change current directory to the directory of this file for loading resources
# This is done to ensure that the app can find the necessary resources
os.chdir(os.path.dirname(__file__))

# Add repo path to sys.path
# This is done to allow the app to import modules from the repository
repo_path = os.path.join(os.path.dirname(__file__), "../../")
sys.path.append(repo_path)

# Import TaskWeaver app and related modules
from taskweaver.app.app import TaskWeaverApp
from taskweaver.memory.attachment import AttachmentType
from taskweaver.memory.type_vars import RoleName
from taskweaver.module.event_emitter import PostEventType, RoundEventType, SessionEventHandlerBase
from taskweaver.session.session import Session

# Initialize TaskWeaver app
# The app is initialized with the project path and the use_local_uri flag set to True
project_path = os.path.join(repo_path, "project")
app = TaskWeaverApp(app_dir=project_path, use_local_uri=True)

# Store session info
# A dictionary is used to store the session information for each user
app_session_dict: Dict[str, Session] = {}

# Function to get the response from the LLM model
# This function takes a user query as input and returns the response from the LLM model
def get_response(user_query: str) -> Generator[str, None, None]:
    """
    Get the response from the LLM model.

    Args:
    user_query (str): The user's query.

    Yields:
    str: The response from the LLM model.
    """
    # Get the user's session ID
    user_session_id = st.session_state.get("id", "default_session")
    
    # Get the session object for the user
    app_session_dict[user_session_id] = app.get_session()
    session = app_session_dict[user_session_id]
    
    # Send the user's query to the LLM model and get the response
    response_round = session.send_message(user_query)
    
    # Yield each response from the LLM model
    for val in response_round.post_list[1:]:
        yield val.message

# Check if the chat history list has been created
# If not, create the chat history list
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Print the chat history for the current session
# This is done to display the conversation history to the user
for message in st.session_state.chat_history:
    if list(message.keys())[0] == "Human":
        # Display the user's message
        with st.chat_message("Human"):
            st.markdown(message["Human"])
    elif list(message.keys())[0] == "AI":
        # Display the AI's response
        with st.chat_message("AI"):
            st.markdown(message["AI"])

# Get the user's query
# This is done using the st.chat_input function
user_query = st.chat_input("Your message", key="message_input")

# Check if the user has entered a query
if user_query is not None and user_query != "":
    # Add the user's query to the chat history
    st.session_state.chat_history.append({"Human": user_query})
    
    # Display the user's query
    with st.chat_message("Human"):
        st.markdown(user_query)
    
    # Get the response from the LLM model
    with st.chat_message("TaskWeaver"):
        # Display the response from the LLM model
        response = st.write_stream(get_response(user_query))
        for response in get_response(user_query):
            # Add the AI's response to the chat history
            st.session_state.chat_history.append({"AI": response})