import os

import pytest

from compaipair.complete.cli_functions import available_models
from compaipair.config.cli_functions import (
    print_cache_location,
    show_api_key,
    save_api_key,
)
from compaipair.types.compaicompletion import CompaiCompletion
from compaipair.utils import NoApiKeyException, api_key_path


def test_available_models_throws_exception_if_no_key_is_saved_and_no_key_in_env(mocker):
    if os.path.exists(api_key_path()):
        os.remove(api_key_path())
    mocker.patch("os.environ", return_value={})
    with pytest.raises(NoApiKeyException):
        available_models()


def test_save_api_key_saves_api_key(capsys):
    api_key = "ThisIsAnAPIKey"
    save_api_key(api_key)
    show_api_key()
    captured = capsys.readouterr().out.strip()
    assert api_key in captured


def test_print_cache_path_prints_cache_path_when_env_variable_set(capsys):
    os.environ["COMPAI_CACHE_PATH"] = "/usr/home/.compaipair"
    print_cache_location()
    captured = capsys.readouterr().out.strip()
    assert captured == "/usr/home/.compaipair"


def test_complete_with_priming_prompts_primed_question(mocker, model):
    priming = "You're great!"
    question = "How can I be greater?"
    mock_generate_text = mocker.patch("google.generativeai.generate_text")
    mocker.patch("compaipair.utils.configure_palm_api")
    completion = CompaiCompletion(
        model, question=question, priming=priming, temperature=0.7
    )

    completion.complete()

    mock_generate_text.assert_called_with(
        prompt=f"You're great!\nHow can I be greater?", model=model, temperature=0.7
    )


def test_complete_with_decorator_prompts_decorated_question(mocker, model):
    question = "How can I be greater?"
    decorator = "Explain what steps are necessary"
    mock_generate_text = mocker.patch("google.generativeai.generate_text")
    mocker.patch("compaipair.utils.configure_palm_api")
    completion = CompaiCompletion(
        model, question=question, decorator=decorator, temperature=0.7
    )

    completion.complete()

    mock_generate_text.assert_called_with(
        prompt=f"How can I be greater?\nExplain what steps are necessary",
        model=model,
        temperature=0.7,
    )
