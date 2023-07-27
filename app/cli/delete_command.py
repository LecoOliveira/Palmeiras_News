import logging
import logging.config

import typer
from rich.console import Console
from typing_extensions import Annotated

from app.cli.config_cli import progress_bar
from app.config.constants import ENV

cli = typer.Typer()

logging.config.fileConfig('app/config/logging.conf')
logger = logging.getLogger('rocketry.task')
console = Console()


@cli.callback(
    invoke_without_command=True,
    help='Comando que deleta uma variável de ambiente do arquivo.',
)
def delete(
    variavel: Annotated[
        str,
        typer.Argument(
            help='Variável que será excluída Ex.: sid, token, '
            'twilio-phone ou destiny-phone',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(help='Arquivo de onde a função vai deletar a variável'),
    ] = ENV,
):
    """
    Comando do CLI que deleta uma variável de ambiente do arquivo.

    Comando: `palmeiras delete VARIÁVEL_QUE_DESEJA_EXCLUIR`

    Args: Argumentos:
        variavel (str): Variável que será excluída.
        env (str): Arquivo de onde a função vai deletar a variável.
    """
    option = {
        'destiny-phone': 'TWILIO_DESTINY_PHONE_NUMBER',
        'sid': 'TWILIO_ACCOUNT_SID',
        'twilio-phone': 'TWILIO_PHONE_NUMBER',
        'token': 'TWILIO_AUTH_TOKEN',
    }

    with open(env, 'r') as arquivo:
        variaveis = arquivo.readlines()

        try:
            for indice, item in enumerate(variaveis):
                if option[variavel] in variaveis[indice]:
                    variaveis.remove(item)
                    progress_bar(description='Removendo...')
                    msg_confirmacao = (
                        f'{option[variavel]} removido com sucesso.'
                    )
                    console.log(f'{msg_confirmacao}\n')
                    logger.info(f'{msg_confirmacao}')
                    with open(env, 'w') as fw:
                        arquivo = fw.write(''.join(variaveis))
                    return
            else:
                raise KeyError

        except KeyError:
            progress_bar(0, description='[b][red]ERRO!!![/red][/b]')
            msg_erro = f'O arquivo não contém nenhum {variavel}.'
            console.log(
                f'\n{msg_erro}\n Tente uma dessas {[*option.keys()]}.'
                'Ou tente um "palmeiras listar" para listar as '
                'variáveis disponíveis.\n'
            )
            logger.error(msg_erro)
