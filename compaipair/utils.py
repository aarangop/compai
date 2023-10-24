import os

import google.generativeai as palm
from google.api_core import retry
from tinydb import TinyDB


class NoApiKeyException(Exception):
    pass


def db_path():
    return os.path.join(get_cache_path(), "db.json")


def db():
    if not os.path.exists(db_path()):
        with open(db_path(), "w"):
            pass
    return TinyDB(db_path())


def get_cache_path(create_if_not_exists: bool = True):
    cache_path = (
        os.environ["COMPAI_CACHE_PATH"]
        if "COMPAI_CACHE_PATH" in os.environ
        else os.path.join(os.path.expanduser("~"), ".compai")
    )
    if not os.path.exists(cache_path) and create_if_not_exists:
        os.mkdir(cache_path)
    return cache_path


def api_key_path():
    return os.path.join(get_cache_path(), "api_key")


def get_api_key():
    try:
        # Load API key
        with open(api_key_path(), "r") as f:
            return f.read()
    except FileNotFoundError:
        raise NoApiKeyException


prompt_template = """
{priming}
{question}
{decorator}
"""


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


def configure_palm_api(fn, *args, **kwargs):
    def wrapper():
        palm.configure(api_key=get_api_key(), transport="rest")
        fn(*args, **kwargs)

    return wrapper


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
