import click

from compaipair.templates.cli_functions import (
    new_template,
    edit_template,
    show_templates,
)


@click.group(name="templates")
def templates_api():
    pass


@templates_api.command(name="new")
@click.argument("name")
@click.option(
    "--priming", "-p", default="", help="Text for priming this template's prompts"
)
@click.option(
    "--decorator", "-d", default="", help="Text for decorating this template's prompts"
)
def new_template_cli(name: str, priming, decorator):
    new_template(name, priming, decorator)


@templates_api.command("edit")
@click.argument("name")
@click.option(
    "--priming", "-p", default="", help="Text for priming this template's prompts"
)
@click.option(
    "--decorator", "-d", default="", help="Text for decorating this template's prompts"
)
def edit_template_cli(name: str, priming: str, decorator: str):
    edit_template(name, priming, decorator)


@templates_api.command("show", help="Show the list of available templates")
@click.option("--name", "-n", default=None, help="Name of the template to show.")
@click.option("--verbose", "-v", default=False, help="Show all the templates' contents")
def show_templates_cli(name, verbose):
    show_templates(name, verbose)
