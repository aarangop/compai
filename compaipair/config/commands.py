import click

from compaipair.config.cli_functions import (
    save_api_key,
    print_cache_location,
    show_api_key,
)


@click.group(name="config")
def config_cli():
    pass


@config_cli.command(name="save_api_key")
@click.argument("api_key")
def save_api_key_cli(api_key):
    save_api_key(api_key)


@config_cli.command(name="show_api_key")
def show_api_key_cli():
    show_api_key()


@config_cli.command(name="cache_location")
def print_cache_location_cli():
    print_cache_location()
