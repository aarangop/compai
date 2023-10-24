from compaipair.cli import compai
from compaipair.complete.commands import complete_cli, available_models_cli
from compaipair.config.commands import config_cli

# Core commands
compai.add_command(complete_cli)
compai.add_command(available_models_cli)

# Config commands
compai.add_command(config_cli)
