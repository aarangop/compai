import os

import pytest
from google.generativeai.types import Model

from compaipair.complete.cli_functions import available_models
from compaipair.config.cli_functions import (
    print_cache_location,
    show_api_key,
    save_api_key,
)
from compaipair.utils import NoApiKeyException


@pytest.fixture
def create_test_env():
    os.environ["COMPAI_CACHE_PATH"] = os.path.join(
        os.path.expanduser("~"), ".compai-test"
    )
    yield
    os.environ["COMPAI_CACHE_PATH"] = os.path.join(os.path.expanduser("~"), ".compai")


@pytest.fixture
def models():
    return [
        Model(
            name="model-1",
            base_model_id="model-1",
            description="AI model 1",
            version="1",
            display_name="model-1",
            input_token_limit=1000,
            output_token_limit=1000,
            supported_generation_methods=["text"],
        ),
        Model(
            name="model-2",
            base_model_id="model-2",
            description="AI model 2",
            version="2",
            display_name="model-2",
            input_token_limit=1000,
            output_token_limit=1000,
            supported_generation_methods=["text"],
        ),
    ]


def test_available_models_prints_available_model_name(mocker, capsys, models):
    mocker.patch("google.generativeai.configure")
    mocker.patch("google.generativeai.list_models", return_value=models)
    mocker.patch("compaipair.utils.get_api_key")
    available_models()
    captured = capsys.readouterr().out
    assert all(
        model_name_output in captured
        for model_name_output in ["name: model-1", "name: model-2"]
    )


def test_available_models_prints_available_model_description(mocker, capsys, models):
    mocker.patch("google.generativeai.configure")
    mocker.patch("google.generativeai.list_models", return_value=models)
    mocker.patch("compaipair.utils.get_api_key")
    available_models()
    captured = capsys.readouterr().out
    assert all(
        model_description_output in captured
        for model_description_output in [
            "description: AI model 1",
            "description: AI model 2",
        ]
    )


def test_available_models_throws_exception_if_no_key_is_provided(mocker):
    with pytest.raises(NoApiKeyException):
        available_models()


def test_save_api_key_saves_api_key(capsys):
    api_key = "ThisIsAnAPIKey"
    save_api_key(api_key)
    show_api_key()
    captured = capsys.readouterr().out.strip()
    assert api_key in captured


def test_print_cache_path_prints_cache_path(mocker, capsys):
    mocker.patch("compaipair.utils.get_cache_path", return_value="/usr/home/.compai")
    print_cache_location()
    captured = capsys.readouterr().out.strip()
    assert captured == "/usr/home/.compai"
