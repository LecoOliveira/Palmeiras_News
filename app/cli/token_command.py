import typer
from typing_extensions import Annotated

from app.cli.config_cli import adicionar_linha
from app.config.constants import ENV

cli = typer.Typer()


@cli.callback(
    invoke_without_command=True,
    help='Configura o TWILI_AUTH_TOKEN na variável de ambiente.',
)
def token(
    token: Annotated[
        str,
        typer.Argument(
            help='Token gerado ao efetuar cadastro na Twilio',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(
            help='Arquivo onde será armazenada a variável de ambiente.'
        ),
    ] = ENV,
):
    """
    Adiciona o TOKEN da conta Twilio na variável de ambiente;

    Comando: `palmeiras token YOUR_TWILIO_AUTH_TOKEN`

    Args: Argumentos:
        token (str): Token gerado ao efetuar cadastro na Twilio.
        env (str): Arquivo onde será armazenada a variável de ambiente.
    """
    adicionar_linha('TWILIO_AUTH_TOKEN', token, env)
