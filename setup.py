from setuptools import setup, find_packages

HOME_URL = "https://github.com/iamaziz/st_ollama"

setup(
    name="ollachat",
    version="0.1.5",
    author="Aziz Alto",
    author_email="iamaziz.alto@gmail.com",
    description="A Streamlit chatbot app integrating Ollama LLMs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=HOME_URL,
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "ollama",
    ],
    package_data={'ollachat': ['chatbot.py']},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ollachat=ollachat.cli:run_streamlit",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
