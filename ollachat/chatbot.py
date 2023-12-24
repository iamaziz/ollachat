import os
import json
import datetime

import streamlit as st
from llama_index.llms import Ollama
from llama_index.llms import ChatMessage
# https://docs.llamaindex.ai/en/stable/examples/llm/ollama.html

from list_ollama_models import OLLAMA_MODELS



def st_ollama(model_name, user_question, chat_history_key):

    llm_ = Ollama(model=model_name)
    
    if chat_history_key not in st.session_state.keys():
        st.session_state[chat_history_key] = []

    print_chat_history_timeline(chat_history_key)
        
    # run the model
    if user_question:
        st.session_state[chat_history_key].append({"content": f"{user_question}", "role": "user"})
        with st.chat_message("question", avatar="🧑‍🚀"):
            st.write(user_question)

        # with st.spinner("Thinking ..."):
        messages = [ChatMessage(content=message["content"], role=message["role"]) for message in st.session_state[chat_history_key]]

        response = llm_.stream_chat(messages)
        
        # streaming response
        with st.chat_message("response", avatar="🤖"):
            chat_box = st.empty()
            response_message = ""
            for chunk in response:
                response_message += chunk.delta
                chat_box.write(response_message)        

        st.session_state[chat_history_key].append({"content": f"{response_message}", "role": "assistant"})
        
        return response_message


def print_chat_history_timeline(chat_history_key):
    for message in st.session_state[chat_history_key]:
        role = message["role"]
        if role == "user":
            with st.chat_message("user", avatar="🧑‍🚀"): 
                question = message["content"]
                st.markdown(f"{question}", unsafe_allow_html=True)
        elif role == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message["content"], unsafe_allow_html=True)


# -- helpers --
def page_config():
    st.set_page_config(layout="wide", page_title="Ollama Chat", page_icon="🦙")
    footer = """<div style="position: fixed; left: 0; bottom: 0; background-color: #004d4d; color: white; padding: 10px 20px; border-top-right-radius: 10px; box-shadow: 2px 2px 5px grey; font-size: 10px; opacity: 0.5;">
                Source code <a href="https://github.com/iamaziz/st_ollama" style="color: white; text-decoration: none; font-weight: bold;">here</a>
                <br>
                <span style="font-size: 10px;">2023 By Aziz Alto</span>
        </div>"""
    st.sidebar.markdown(footer, unsafe_allow_html=True)


def assert_models_installed():
    if len(OLLAMA_MODELS) < 1:
        st.sidebar.warning("No models found. Please install at least one model e.g. `ollama run llama2`")
        st.stop()


def save_conversation(llm_name, conversation_key):

    OUTPUT_DIR = "llm_conversations"
    OUTPUT_DIR = os.path.join(os.getcwd(), OUTPUT_DIR)

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{OUTPUT_DIR}/{timestamp}_{llm_name.replace(':', '-')}"

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    if st.session_state[conversation_key]:

        if st.sidebar.button("Save conversation"):
            with open(f"{filename}.json", "w") as f:
                json.dump(st.session_state[conversation_key], f, indent=4)
            st.success(f"Conversation saved to {filename}.json")


if __name__ == "__main__":

    page_config()
    
    st.sidebar.title("Ollama Chat 🦙")
    llm_name = st.sidebar.selectbox("Choose Agent", [""] + OLLAMA_MODELS)
    
    assert_models_installed()
    
    if not llm_name: st.stop()

    conversation_key = f"model_{llm_name}"
    prompt = st.chat_input(f"Ask '{llm_name}' a question ...")

    st_ollama(llm_name, prompt, conversation_key)
    
    if st.session_state[conversation_key]:
        clear_conversation = st.sidebar.button("Clear chat")
        if clear_conversation:
            st.session_state[conversation_key] = []
            st.rerun()

    # save conversation to file
    save_conversation(llm_name, conversation_key)