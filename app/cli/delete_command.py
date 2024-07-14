import typer
from rich.console import Console
from typing_extensions import Annotated

from app.cli.config_cli import log_mensagem, progress_bar
from app.config.settings import Settings

cli = typer.Typer()

settings = Settings()
console = Console()


@cli.callback(
    invoke_without_command=True,
    help='Comando que deleta uma variável de ambiente do arquivo.',
)
def delete(
    variavel: Annotated[
        str,
        typer.Argument(
            help='Variável que será excluída Ex.: id, token',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(help='Arquivo de onde a função vai deletar a variável'),
    ] = settings.ENV,
):
    """
    Comando do CLI que deleta uma variável de ambiente do arquivo.

    Comando: `palmeiras delete VARIÁVEL_QUE_DESEJA_EXCLUIR`

    Args: Argumentos:
        variavel (str): Variável que será excluída.
        env (str): Arquivo de onde a função vai deletar a variável.
    """
    option = {
        'id': 'BOT_ID',
        'token': 'BOT_TOKEN',
    }

    with open(env, 'r') as arquivo:
        variaveis = arquivo.readlines()

        try:
            for indice, item in enumerate(variaveis):
                if option[variavel] in variaveis[indice]:
                    variaveis.remove(item)
                    progress_bar(description='Removendo...')
                    log_mensagem(
                        'info', f'{option[variavel]} removido com sucesso.'
                    )
                    with open(env, 'w') as fw:
                        arquivo = fw.write(''.join(variaveis))
                    return
            else:
                raise KeyError

        except KeyError:
            progress_bar(0, description='[b][red]ERRO!!![/red][/b]')
            log_mensagem('erro', f'O arquivo não contém nenhum {variavel}.')
            console.log(
                f'\n Tente uma dessas {[*option.keys()]}. '
                'Ou tente "palmeiras listar" para listar as '
                'variáveis disponíveis.\n'
            )
