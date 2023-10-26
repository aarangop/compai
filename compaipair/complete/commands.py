import click

from compaipair.complete.cli_functions import complete, available_models


@click.command(name="complete")
@click.option("--priming", help="String to prime the LLM prompt")
@click.option("--decorator", help="Decorator to your prompt")
@click.option("-o", "--output", default="./result.md", help="File to write output")
@click.option(
    "-i",
    "--input-file",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="File with input to append to the question.",
)
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
@click.option(
    "--plain-text",
    is_flag=True,
    default=False,
    help="Print output in plain text, otherwise will be formatted as Markdown",
)
@click.option(
    "--template",
    default=None,
    type=click.STRING,
    help="Template to prime and decorate prompt.",
)
@click.argument("question")
def complete_cli(
    question,
    priming,
    decorator,
    input_file,
    output,
    temperature,
    model_name,
    verbose,
    plain_text,
    template,
):
    complete(
        question=question,
        priming=priming,
        decorator=decorator,
        output=output,
        temperature=temperature,
        model_name=model_name,
        verbose=verbose,
        plain_text_output=plain_text,
        template=template,
        input_file=input_file,
    )


@click.command("complete-template")
@click.argument("template")
@click.option(
    "-q", "--question", help="Optional question that will be appended to the template."
)
@click.option("-o", "--output", default="./result.md", help="File to write output")
@click.option(
    "-i",
    "--input-file",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="File with input to append to the question.",
)
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
@click.option(
    "--plain-text",
    is_flag=True,
    default=False,
    help="Print output in plain text, otherwise will be formatted as Markdown",
)
def complete_template_cli(
    question,
    priming,
    decorator,
    input_file,
    output,
    temperature,
    model_name,
    verbose,
    plain_text,
    template,
):
    complete(
        input_file=input_file,
        question=question,
        priming=priming,
        decorator=decorator,
        output=output,
        temperature=temperature,
        model_name=model_name,
        verbose=verbose,
        plain_text_output=plain_text,
        template=template,
    )


@click.command(name="available-models")
def available_models_cli():
    available_models()
