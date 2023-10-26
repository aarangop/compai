import click

from compaipair.config.cli_functions import (
    save_api_key,
    print_cache_location,
    show_api_key,
    init,
)


@click.group(name="config")
def config_api():
    pass


@config_api.command(name="save-api-key")
@click.argument("api_key")
def save_api_key_cli(api_key):
    save_api_key(api_key)


@config_api.command(name="show-api-key")
def show_api_key_cli():
    show_api_key()


@config_api.command(name="show-cache-location")
def print_cache_location_cli():
    print_cache_location()


@config_api.command(name="init")
@click.option("--api-key", help="Google MakerSuite's API Key")
def init_cli(api_key: str):
    init(api_key=api_key)
