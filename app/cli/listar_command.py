import logging
import logging.config

import typer
from rich.console import Console
from typing_extensions import Annotated

from app.config.settings import Settings

cli = typer.Typer()
console = Console()
settings = Settings()
logging.config.fileConfig('app/config/logging.conf')
logger = logging.getLogger('rocketry.task')


@cli.callback(
    invoke_without_command=True,
    help=('Lista todas as variáveis de ambiente cadastradas'),
)
def listar(
    id: Annotated[
        bool,
        typer.Option(
            help='Lista o BOT_ID configurado no arquivo de variável;',
            show_default=False,
        ),
    ] = False,
    token: Annotated[
        bool,
        typer.Option(
            help='Lista o BOT_TOKEN configurado no arquivo de variável;',
            show_default=False,
        ),
    ] = False,
    env: Annotated[
        str,
        typer.Option(help='Arquivo de onde será lido a variável de ambiente'),
    ] = settings.ENV,
):
    """
    Lista todas as variáveis de ambiente cadastradas.

    Exemplos:
        Para listar todas as variáveis:
        ```bash
        $ palmeiras listar

        [15:13:50]  BOT_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                    BOT_ID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        ```
        Para listar uma variável específica:
        ```bash
        $ palmeiras listar --token

        [11:41:16] BOT_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        ```

    Opções: `--token, --id`

    Args: Argumentos:
        token (bool): Lista o TWILIO_AUTH_TOKEN configurado no arquivo de variável.
        id (bool): Lista o SID configurado no arquivo de variável.
        env (str): Arquivo de onde buscar as variáveis.
    """

    option = {id: 'BOT_ID', token: 'BOT_TOKEN'}.get(True, None)

    if option is None:
        try:
            with open(env, 'r') as arquivo:
                console.log(f'\n{"".join(arquivo)}')
            return

        except FileNotFoundError:
            console.log(
                f'\nNenhum arquivo {env} encontrado.\n'
                'Tente sem o "--env", ou rode "palmeiras listar '
                '--help" para obter ajuda.\n'
            )
            logger.error(f'Nenhum arquivo {env} encontrado.')
            return

    try:
        with open(env, 'r') as arquivo:
            linhas = arquivo.readlines()
            valores = [linha for linha in linhas if option in linha]
            if valores:
                console.log(f'\n{"".join(valores)}\n')
            else:
                console.log(
                    f'\nNenhuma variável de ambiente "{option}" encontrada.\n'
                    f'Para cadastrar tente:'
                    f'\npalmeiras [OPTION] [ARG] ou palmeiras --help\n'
                )
                logger.error(
                    f'Nenhuma variável de ambiente "{option}" encontrada.'
                )

    except IOError:
        console.log(
            '\nErro ao ler o arquivo. Você deve configurar alguma '
            'variável antes de tentar listá-las\n'
        )
        logger.warning(f'Erro ao ler o arquivo.')
