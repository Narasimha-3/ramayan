import streamlit as st
from utils import get_result, detectlanguageandanswer

Nodes = ["No Nodes Yet"]

def lab():
    global Nodes

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
            response1, Nodes = get_result(prompt)
            response = detectlanguageandanswer(prompt)
            # print(response)
            # Display assistant response in chat message container
            
            with st.chat_message("assistant"):
                st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def nods():
    st.write(Nodes)