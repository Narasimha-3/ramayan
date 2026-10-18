from pickle import TRUE
import streamlit as st
import json
import random
import string
from datetime import datetime
import streamlit as st

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
    ans = ""
    with open("log.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            ans += line + "\n"
    st.title("**:orange[Ramayana]** Chunks")
    st.markdown(ans)

def query_variants():
    ans = ""
    with open("query_variants.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            ans += line + "\n"
    st.title("**:orange[Ramayana]** Query Variants")
    st.markdown(ans)

def verses():
    ans = ""
    with open("verses_retrieved.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            ans += line + "\n"
    st.title("**:orange[Ramayana]** Verses")
    st.markdown(ans)

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
    prompt = st.chat_input("<kanda>: <question> - for detailed answer in that kanda")
    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.spinner("Fetching..."):
            import requests
            if prompt.split(":")[0] in ["balakanda", "ayodhyakanda", "aranyakanda", "kishkindhakanda", "sundarakanda", "yuddhakanda", "uttarakanda"]:
                URL = "http://127.0.0.1:8000/kg_mini"
                PARAMS = {
                    'item': prompt
                    }
                r = requests.post(url = URL, params = PARAMS)
                response = r.json()
            else:
                URL = "http://127.0.0.1:8000/kg"
                PARAMS = {
                    'item': prompt
                    }
                r = requests.post(url = URL, params = PARAMS)
                response = r.json()                
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})