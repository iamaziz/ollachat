import os
import json
import datetime

import streamlit as st
import ollama


try:
    OLLAMA_MODELS = ollama.list()["models"]
except Exception as e:
    st.warning("Please make sure Ollama is installed first. See https://ollama.ai for more details.")
    st.stop()




def st_ollama(model_name, user_question, chat_history_key):

    
    if chat_history_key not in st.session_state.keys():
        st.session_state[chat_history_key] = []

    print_chat_history_timeline(chat_history_key)
        
    # run the model
    if user_question:
        st.session_state[chat_history_key].append({"content": f"{user_question}", "role": "user"})
        with st.chat_message("question", avatar="🧑‍🚀"):
            st.write(user_question)

        messages = [dict(content=message["content"], role=message["role"]) for message in st.session_state[chat_history_key]]

        def llm_stream(response):
            response = ollama.chat(model_name, messages, stream=True)
            for chunk in response:
                yield chunk['message']['content']

        # streaming response
        with st.chat_message("response", avatar="🤖"):
            chat_box = st.empty()
            response_message = chat_box.write_stream(llm_stream(messages))

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



def assert_models_installed():
    if len(OLLAMA_MODELS) < 1:
        st.sidebar.warning("No models found. Please install at least one model e.g. `ollama run llama2`")
        st.stop()


def select_model():
    
    model_names = [model["name"] for model in OLLAMA_MODELS]
    
    llm_name = st.sidebar.selectbox(f"Choose Agent (available {len(model_names)})", [""] + model_names)
    if llm_name:

        # llm details object
        llm_details = [model for model in OLLAMA_MODELS if model["name"] == llm_name][0]

        # convert size in llm_details from bytes to GB (human-friendly display)
        if type(llm_details["size"]) != str:
            llm_details["size"] = f"{round(llm_details['size'] / 1e9, 2)} GB"

        # display llm details
        with st.expander("LLM Details"):
            st.write(llm_details)

        return llm_name


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

    st.set_page_config(layout="wide", page_title="Ollama Chat", page_icon="🦙")

    st.sidebar.title("Ollama Chat 🦙")
    llm_name = select_model()
    
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