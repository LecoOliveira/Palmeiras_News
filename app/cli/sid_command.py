import typer
from typing_extensions import Annotated

from app.cli.config_cli import adicionar_linha
from app.config.constants import ENV

cli = typer.Typer()


@cli.callback(
    invoke_without_command=True,
    help='Configura o TWILIO_ACCOUNT_SID na variável de ambiente.',
)
def sid(
    sid: Annotated[
        str,
        typer.Argument(
            help='Seu SID gerado ao efetuar cadastro na Twilio',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(
            help='Arquivo que será armazenada a variável de ambiente'
        ),
    ] = ENV,
):
    """
    Adiciona o SID da conta Twilio na variável de ambiente;

    Comando: `palmeiras sid YOUR_TWILIO_ACCOUNT_SID`

    Args: Argumentos:
        sid (str): Seu SID gerado ao efetuar cadastro na Twilio.
        env (str): Arquivo que será armazenada a variável de ambiente.
    """
    adicionar_linha('TWILIO_ACCOUNT_SID', sid, env)
