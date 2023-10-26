from compaipair.cli import compai
from compaipair.complete.commands import (
    complete_cli,
    available_models_cli,
    complete_template_cli,
)
from compaipair.config.commands import config_api
from compaipair.templates.commands import templates_api

# Core commands
compai.add_command(complete_cli)
compai.add_command(available_models_cli)
compai.add_command(complete_template_cli)

# Config commands
compai.add_command(config_api)

# Templates commands
compai.add_command(templates_api)
