import os

import google.generativeai as palm
from google.api_core import retry
from tinydb import TinyDB

from compaipair.types.exceptions import NoApiKeyException

prompt_template = """
{priming}
{question}
{decorator}
"""


def db_path():
    return os.path.join(get_cache_path(), "db.json")


def get_db() -> TinyDB:
    if not os.path.exists(db_path()):
        with open(db_path(), "w"):
            pass
    if get_db.db is None:
        get_db.db = TinyDB(db_path())
    return get_db.db


get_db.db = None


def close_db():
    if get_db.db is not None:
        get_db().close()
    get_db.db = None


def get_cache_path():
    return (
        os.environ["COMPAI_CACHE_PATH"]
        if "COMPAI_CACHE_PATH" in os.environ
        else os.path.join(os.path.expanduser("~"), ".compai")
    )


def create_cache_dir():
    cache_path = get_cache_path()
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)


def get_available_models():
    return palm.list_models()


def api_key_path():
    return os.path.join(get_cache_path(), "api_key")


def get_api_key() -> str:
    """Gets the API key for the Google Generative AI API.

    First, tries to load the API key from the environment variable
    `GOOGLE_GENERATIVEAI_API_KEY`. If that fails, tries to load the API key
    from the cache directory.
    :raises: `NoApiKeyException`.

    Returns:
        str: The API key.
    """
    # Try to load api key from environment
    if "GOOGLE_GENERATIVEAI_API_KEY" in os.environ:
        return os.environ["GOOGLE_GENERATIVEAI_API_KEY"]
    try:
        # Load API key from file
        with open(api_key_path(), "r") as f:
            return f.read()
    except FileNotFoundError:
        raise NoApiKeyException


def try_read_file(potential_path):
    if potential_path is None:
        return None
    if os.path.exists(potential_path):
        with open(potential_path, "r") as f:
            return f.read()
    return None


def get_prompt(priming: str, question: str, decorator: str):
    priming_file_contents = try_read_file(priming)
    if priming_file_contents is not None:
        priming = priming_file_contents

    question_file_contents = try_read_file(question)
    if question_file_contents is not None:
        question = question_file_contents

    decorator_file_contents = try_read_file(decorator)
    if decorator_file_contents is not None:
        decorator = decorator_file_contents

    return prompt_template.format(
        priming=priming, question=question, decorator=decorator
    )


def prompt_code(priming: str, code_file: str, decorator: str):
    with open(code_file, "r") as f:
        code = f.read()
    return prompt_template.format(priming=priming, question=code, decorator=decorator)


def configure_palm_api(api_key: str = None):
    if api_key is None:
        api_key = get_api_key()
    if api_key is None:
        raise NoApiKeyException
    palm.configure(api_key=api_key, transport="rest")


def print_completion_results(completion, prompt=None):
    if prompt:
        print("Completion generated for prompt: \n")
        print(prompt)
        print("########################################\n\n")
    print("Completion: \n")
    print(completion.result)


@retry.Retry()
def generate_text(prompt, model, temperature=0.0):
    return palm.generate_text(prompt=prompt, model=model, temperature=temperature)
