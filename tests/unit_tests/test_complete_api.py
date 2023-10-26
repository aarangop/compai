from dataclasses import dataclass

from compaipair.complete.cli_functions import complete, available_models


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


def test_complete_with_question_outputs_an_answer(capsys, mocker):
    @dataclass
    class ResultMock:
        result: str

    question = "What's the meaning of life, the universe and everything?"
    response = "The answer to life, the universe, and everything is 42"
    mocker.patch(
        "compaipair.types.compaicompletion.palm.generate_text",
        return_value=ResultMock(result=response),
    )

    complete(question=question)

    capture = capsys.readouterr().out.strip()
    assert response in capture


def test_complete_with_priming_and_decorator_prompts_model_with_primed_and_decorated_question(
    mocker, capsys
):
    @dataclass
    class ResultMock:
        result: str

    priming = "You're an old man who's very wise"
    question = "What's the meaning of life, the universe and everything?"
    decorator = "Please tell me why"

    response = "The answer to life, the universe, and everything is 42"
    mocker.patch(
        "compaipair.types.compaicompletion.palm.generate_text",
        return_value=ResultMock(result=response),
    )

    complete(question=question, priming=priming, decorator=decorator, verbose=True)

    capture = capsys.readouterr().out.strip()
    assert all(
        [expected_text in capture for expected_text in [priming, question, decorator]]
    )
