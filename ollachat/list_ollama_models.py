import re
import subprocess


def _parse_names(data: str) -> list[str]:
    """
    Parses names from a multi-line string where each line contains a name and other details.

    Parameters:
    data (str): A multi-line string containing names and other details.

    Returns:
    list: A list containing the parsed names.
    """
    # Split the string into lines
    lines = data.strip().split("\n")

    # Skip the header line
    lines = lines[1:]

    # Regex pattern to match the name at the beginning of each line
    pattern = r"^\S+"

    # Extract names using regex
    names = [
        re.match(pattern, line).group(0) for line in lines if re.match(pattern, line)
    ]

    return names


def _run_commandline(command: str) -> str:
    """
    Runs a commandline command and returns the output.

    Parameters:
    command (str): A string containing the command to be run.

    Returns:
    str: A string containing the output from the command.
    """

    command = command.split(" ")

    # Run the command
    result = subprocess.run(command, capture_output=True)

    # Get the output
    output = result.stdout.decode("utf-8")

    return output


def list_models() -> list[str]:
    """
    Lists all available OLLAMA models.

    Parameters:
    None

    Returns:
    None
    """
    # Run the command, and assert ollama is installed

    try:
        data = _run_commandline("ollama list")
    except FileNotFoundError as e:
        raise FileNotFoundError(
            "Unable to find Ollama command. Please install OLLAMA first. See https://ollama.ai for more details.")

    # Parse the names
    names = _parse_names(data)

    # assert len(names) < 0, "No models found. Please install OLLAMA first."


    return sorted(names)


OLLAMA_MODELS = list_models()

if __name__ == "__main__":
    # get list of names
    names = list_models()
    print(names)
