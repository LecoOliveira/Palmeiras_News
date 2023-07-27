import logging
import logging.config
from re import compile
from typing import List

import typer
from rich.console import Console
from typing_extensions import Annotated

from app.cli.config_cli import adicionar_linha
from app.config.constants import ENV

cli = typer.Typer()

logging.config.fileConfig('app/config/logging.conf')
logger = logging.getLogger('rocketry.task')
console = Console()


@cli.callback(
    invoke_without_command=True,
    help='Configura os números para onde serão enviadas as mensagens.',
)
def destiny_phone(
    phones: Annotated[
        List[str],
        typer.Argument(
            help='Um ou mais destiny_phone que deseja configurar '
            '(números devem ser separados por espaço); '
            'Ex: +551199999999 +5511999999999',
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
    Adiciona números de destino para onde serão enviadas as mensagens;

    Comando: `palmeiras destiny-phone YOUR_TWILIO_DESTINY_PHONES`

    Args: Argumentos:
        phones (List[str]): Um ou mais telefones que deseja configurar para que possam receber as mensagens (números devem ser separados por espaço) Ex: +551199999999 +5511999999999.
        env (str): Arquivo que será armazenada a variável de ambiente.
    """
    padrao = compile(r'^\+\d{2,3}\d{2}\d{4,5}\d{4}$')

    numeros_validos = [
        phone
        for indice, phone in enumerate(phones)
        if padrao.match(phones[indice])
    ]

    numeros_invalidos = list(
        filter(lambda phone: phone not in numeros_validos, phones)
    )

    if numeros_invalidos:
        msg_erro = f'Número(s) {" ".join(numeros_invalidos)} inválido(s).'
        console.log(
            f'\n{msg_erro} '
            'O número deve conter o formato +xxxxxxxxxxxxx '
            '(Começando com o sinal "+" e ter entre 12 e 14 números).\n'
        )
        logger.error(f'{msg_erro}')
        return

    adicionar_linha('TWILIO_DESTINY_PHONE_NUMBER', numeros_validos, env)
