import typer

from app.cli import (
    bot_token_command,
    config_cli,
    delete_command,
    listar_command,
)

app = typer.Typer()

app.add_typer(bot_token_command.cli, name='bot_token')
app.add_typer(delete_command.cli, name='delete')
app.add_typer(listar_command.cli, name='listar')
