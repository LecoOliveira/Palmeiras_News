import typer

from app.cli import (
    config_cli,
    delete_command,
    destiny_phone_command,
    listar_command,
    sid_command,
    token_command,
    twilio_phone_command,
)

app = typer.Typer()

app.add_typer(sid_command.cli, name='sid')
app.add_typer(token_command.cli, name='token')
app.add_typer(twilio_phone_command.cli, name='twilio-phone')
app.add_typer(destiny_phone_command.cli, name='destiny-phone')
app.add_typer(delete_command.cli, name='delete')
app.add_typer(listar_command.cli, name='listar')
