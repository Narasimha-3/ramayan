from pickle import TRUE
import streamlit as st
import json
import random
import string
from datetime import datetime
import streamlit as st
from utils import get_result

puli = False
blud_data = {}


def set_page_container_style(
        max_width: int = 1100, max_width_100_percent: bool = False,
        padding_top: int = 1, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = 10,
        color: str = "blue", background_color: str = "black",
    ):
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'
        st.markdown(
            f'''
            <style>
                .reportview-container .sidebar-content {{
                    padding-top: {padding_top}rem;
                }}
                .reportview-container .main .block-container {{
                    {max_width_str}
                    padding-top: 0rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
                .reportview-container .main {{
                    color: {color};
                    background-color: {background_color};
                }}
            </style>
            ''',
            unsafe_allow_html=True,
        )

def chunks():
    st.title("Chunks")
    st.write("Chunks are the smaller parts of the data that is retrived from the ramayan")
    st.write("Chunks are the smaller parts of the data that is retrived from the ramayan")
    st.write("Chunks are the smaller parts of the data that is retrived from the ramayan")
    st.write("Chunks are the smaller parts of the data that is retrived from the ramayan")
    st.write("Chunks are the smaller parts of the data that is retrived from the ramayan")
    st.write("Chunks are the smaller parts of the data that is retrived from the ramayan")
    st.write("Chunks are the smaller parts of the data that is retrived from the ramayan")
    st.write("Chunks are the smaller parts of the data that is retrived from the ramayan")
    st.write("Chunks are the smaller parts of the data that is retrived from the ramayan")
    st.write("Chunks are the smaller parts of the data that is retrived from the ramayan")

def lab():

    st.title("**:orange[Ramayana]** Gpt")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    prompt = st.chat_input("Help with ramayan?")
    if prompt:
    # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
    # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Fetching..."):
            import requests
            URL = "http://127.0.0.1:8000/post"
            PARAMS = {'post':prompt}
            r = requests.post(url = URL, params = PARAMS)
            print(r.text)
            response = r.text
            print(response)
            with st.chat_message("assistant"):
                st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})





def nods():
    st.write("Nodes")