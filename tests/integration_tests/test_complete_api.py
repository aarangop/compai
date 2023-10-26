import os

import pytest
from dotenv import load_dotenv

from compaipair.complete.cli_functions import available_models, complete

load_dotenv()


@pytest.fixture(autouse=True)
def load_api_key_to_env():
    prev_api_key = (
        os.environ["GOOGLE_GENERATIVEAI_API_KEY"]
        if "GOOGLE_GENERATIVEAI_API_KEY" in os.environ
        else None
    )
    os.environ["GOOGLE_GENERATIVEAI_API_KEY"] = os.environ[
        "TEST_GOOGLE_GENERATIVEAI_API_KEY"
    ]
    yield
    if prev_api_key is not None:
        os.environ["GOOGLE_GENERATIVEAI_API_KEY"] = prev_api_key


def test_available_models_prints_available_models(capsys):
    available_models()
    captured = capsys.readouterr().out.strip()

    assert all(
        [
            expected_text in captured
            for expected_text in ["name", "description", "generation methods"]
        ]
    )


def test_complete_api_prints_a_result(capsys):
    complete(
        priming="You're an experienced python programming that likes using pytests for their unit tests",
        question="Could you generate a test case for a class that prompts an AI model?",
        decorator="Please comment each line of your code",
    )

    captured = capsys.readouterr().out.strip()

    assert "None" != captured
