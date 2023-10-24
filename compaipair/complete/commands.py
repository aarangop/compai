import click

from compaipair.complete.cli_functions import complete, available_models


@click.command
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
@click.argument("question")
def complete_cli(**kwargs):
    complete(**kwargs)


@click.command(name="available_models")
def available_models_cli():
    available_models()
