import os
from dataclasses import dataclass

import pytest

from compaipair.complete.cli_functions import complete, available_models
from compaipair.types.completion_template import CompletionTemplate
from compaipair.utils import get_cache_path


@pytest.fixture
def patch_generate_text(mocker):
    @dataclass
    class ResultMock:
        result: str

    response = "The answer to life, the universe, and everything is 42"
    mocker.patch(
        "compaipair.types.compaicompletion.palm.generate_text",
        return_value=ResultMock(result=response),
    )
    yield


@pytest.fixture
def patch_get_available_models(mocker, models):
    mocker.patch(
        "compaipair.types.compaicompletion.get_available_models", return_value=models
    )


@pytest.fixture
def patch_complete_api_google_generativeai_methods(
    patch_get_available_models, patch_generate_text
):
    yield


def test_available_models_outputs_list_of_models(capsys, mocker, model):
    mocker.patch("compaipair.complete.cli_functions.configure_palm_api")
    mocker.patch(
        "compaipair.complete.cli_functions.get_available_models",
        return_value=[model],
    )

    available_models()

    capture = capsys.readouterr().out.strip()
    assert all(
        [
            expected_text in capture
            for expected_text in ["model-1", "AI model 1", "text"]
        ]
    )


def test_available_models_prints_available_model_name(mocker, capsys, models):
    mocker.patch("compaipair.complete.cli_functions.configure_palm_api")
    mocker.patch(
        "compaipair.complete.cli_functions.get_available_models", return_value=models
    )

    available_models()

    captured = capsys.readouterr().out
    assert all(
        model_name_output in captured
        for model_name_output in ["name: model-1", "name: model-2"]
    )


def test_available_models_prints_available_model_description(mocker, capsys, models):
    mocker.patch("compaipair.complete.cli_functions.configure_palm_api")
    mocker.patch(
        "compaipair.complete.cli_functions.get_available_models", return_value=models
    )

    available_models()

    captured = capsys.readouterr().out
    assert all(
        model_description_output in captured
        for model_description_output in [
            "description: AI model 1",
            "description: AI model 2",
        ]
    )


def test_complete_with_question_outputs_an_answer(capsys, mocker, models):
    @dataclass
    class ResultMock:
        result: str

    question = "What's the meaning of life, the universe and everything?"
    response = "The answer to life, the universe, and everything is 42"
    mocker.patch(
        "compaipair.types.compaicompletion.palm.generate_text",
        return_value=ResultMock(result=response),
    )
    mocker.patch(
        "compaipair.types.compaicompletion.get_available_models", return_value=models
    )

    complete(question=question)

    capture = capsys.readouterr().out.strip()
    assert response in capture


def test_complete_with_priming_prompts_model_with_primed_question(
    mocker, capsys, models
):
    @dataclass
    class ResultMock:
        result: str

    priming = "You're an old man who's very wise."
    question = "What's the meaning of life, the universe and everything?"

    response = "The answer to life, the universe, and everything is 42"
    mocker.patch(
        "compaipair.types.compaicompletion.palm.generate_text",
        return_value=ResultMock(result=response),
    )
    mocker.patch(
        "compaipair.types.compaicompletion.get_available_models", return_value=models
    )

    complete(
        question=question,
        priming=priming,
        verbose=True,
        plain_text_output=True,
    )

    capture = capsys.readouterr().out.strip()
    assert f"{priming}\n{question}" in capture


def test_complete_with_decorator_prompts_model_with_decorated_question(
    mocker, capsys, models
):
    @dataclass
    class ResultMock:
        result: str

    question = "What's the meaning of life, the universe and everything?"
    decorator = "Please tell me why."

    response = "The answer to life, the universe, and everything is 42"
    mocker.patch(
        "compaipair.types.compaicompletion.palm.generate_text",
        return_value=ResultMock(result=response),
    )
    mocker.patch(
        "compaipair.types.compaicompletion.get_available_models", return_value=models
    )

    complete(
        question=question,
        decorator=decorator,
        verbose=True,
        plain_text_output=True,
    )

    capture = capsys.readouterr().out.strip()
    assert f"{question}\n{decorator}" in capture


def test_complete_with_priming_and_decorator_prompts_model_with_primed_and_decorated_question(
    patch_complete_api_google_generativeai_methods, capsys, models
):
    priming = "You're an old man who's very wise."
    question = "What's the meaning of life, the universe and everything?"
    decorator = "Please tell me why."

    complete(
        question=question,
        priming=priming,
        decorator=decorator,
        verbose=True,
        plain_text_output=True,
    )

    capture = capsys.readouterr().out.strip()
    assert f"{priming}\n{question}\n{decorator}" in capture


def test_complete_with_template_uses_template_priming(
    patch_complete_api_google_generativeai_methods, capsys
):
    CompletionTemplate(
        name="test_template", priming="Yees, you behind the fence!"
    ).save()

    complete(question="Stand still laddie!", template="test_template", verbose=True)

    captured = capsys.readouterr().out.strip()
    assert "Yees, you behind the fence!" in captured


@pytest.fixture
def test_input_file():
    input_path = os.path.join(get_cache_path(), "test_input.txt")
    with open(input_path, "w"):
        pass
    yield input_path

    os.remove(input_path)


def test_complete_with_input_appends_file_contents_to_the_prompt(
    patch_complete_api_google_generativeai_methods, capsys, test_input_file
):
    with open(test_input_file, "w") as f:
        f.write("These are some lines of code")

    complete(question="Heey yooo", input=test_input_file, verbose=True)
    captured = capsys.readouterr().out

    assert "These are some lines of code" in captured
