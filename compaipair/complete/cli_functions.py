from rich.console import Console
from rich.markdown import Markdown

from compaipair.types.compaicompletion import CompaiCompletion
from compaipair.utils import configure_palm_api, get_available_models

console = Console()


def available_models():
    configure_palm_api()
    for m in get_available_models():
        print(f"# {m.name}")
        print(f"description: {m.description}")
        print(f"generation methods: {m.supported_generation_methods}\n\n")


def complete(
    question: str,
    priming: str = "",
    decorator: str = "",
    model_name: str = None,
    temperature: float = 0.7,
    verbose: bool = False,
    output: str = None,
):
    completion = CompaiCompletion(
        question=question,
        priming=priming,
        decorator=decorator,
        model=model_name,
        temperature=temperature,
    )
    completion.complete()

    if completion.result.result is not None:
        completion_result = completion.result.result
        if verbose:
            completion_result = (
                f"# Prompt\n{completion.prompt}\n---\n# Result\n{completion_result}"
            )

        console.print(Markdown(completion_result))
