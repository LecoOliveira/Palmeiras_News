import typer
from typing_extensions import Annotated

from app.cli.config_cli import adicionar_linha
from app.config.constants import ENV

cli = typer.Typer()


@cli.callback(
    invoke_without_command=True,
    help='Configura o TWILIO_PHONE_NUMBER na variável de ambiente.',
)
def twilio_phone(
    phone: Annotated[
        str,
        typer.Argument(
            help='Número americano gerado pela Twilio',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(
            help='Arquivo onde será configurado o TWILIO_PHONE_NUMBER.'
        ),
    ] = ENV,
):
    """
    Adiciona o seu PHONE_NUMBER da conta Twilio na variável de ambiente;

    Comando: `palmeiras twilio-phone YOUR_TWILIO_PHONE`

    Args: Argumentos:
        phone (str): Número americano gerado pela Twilio.
        env (str): Arquivo onde será configurado o TWILIO_PHONE_NUMBER.
    """
    adicionar_linha('TWILIO_PHONE_NUMBER', phone, env)
