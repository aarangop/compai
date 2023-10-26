import click

from compaipair.complete.cli_functions import complete, available_models


@click.command(name="complete")
@click.option("--priming", help="String to prime the LLM prompt")
@click.option("--decorator", help="Decorator to your prompt")
@click.option("-o", "--output", default="./result.md", help="File to write output")
@click.option(
    "-t",
    "--temperature",
    default=0.7,
    help="Model temperature, use 0 for more deterministic completions.",
)
@click.option(
    "-m", "--model-name", default="text-bison-001", help="LLM model for this query"
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Verbose. Include prompt in output",
)
@click.argument("question")
def complete_cli(
    question, priming, decorator, output, temperature, model_name, verbose
):
    complete(
        question=question,
        priming=priming,
        decorator=decorator,
        output=output,
        temperature=temperature,
        model_name=model_name,
        verbose=verbose,
    )


@click.command(name="available-models")
def available_models_cli():
    available_models()
