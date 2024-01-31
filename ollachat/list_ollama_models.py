from functools import lru_cache

import ollama


@lru_cache(maxsize=2)
def list_models():
    models = ollama.list()["models"]
    install_msg = "Please make sure Ollama is installed first. See https://ollama.ai for more details."
    assert len(models) > 0, f"No models found. {install_msg}"
    return models


OLLAMA_MODELS = list_models()


if __name__ == "__main__":
    # get list of names
    names = [model["name"] for model in OLLAMA_MODELS]
    print(names)