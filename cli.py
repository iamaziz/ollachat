import subprocess
import os

def run_streamlit():
    # Get the directory where the package is installed
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chatbot_path = os.path.join(dir_path, 'ollachat/chatbot.py')

    # Run the command
    subprocess.run(["streamlit", "run", chatbot_path])
