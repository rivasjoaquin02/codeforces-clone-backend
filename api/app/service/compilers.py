import os

folder_path = "/shared"

def compile(code: str, lang: str):
    """Compile the code and return the output."""

    os.makedirs(folder_path, exist_ok=True)