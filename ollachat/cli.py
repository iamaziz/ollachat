import subprocess
import os

def run_streamlit():
    # Get the directory where the package is installed
    dir_path = os.path.dirname(os.path.realpath(__file__))
    chatbot_path = os.path.join(dir_path, 'chatbot.py')

    # Run the command
    try:
        subprocess.run(["streamlit", "run", chatbot_path])
    except KeyboardInterrupt:
       print("Shutting down the Streamlit app...")
       exit(0)