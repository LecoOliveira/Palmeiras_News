import logging
import logging.config
import os
import time
from typing import List

from rich.console import Console
from rich.progress import track

from app.config.settings import Settings

logging.config.fileConfig('app/config/logging.conf')
logger = logging.getLogger('rocketry.task')
settings = Settings()
console = Console()


def progress_bar(
    time_: float = 0.02, description: str = 'Configurando...'
) -> None:
    """
    Cria barra de progresso.

    Args: Argumentos:
        time_ (float, optional): Tempo de duração da barra. Padrão 0.02.
        description (str, optional): Mensagem que aparece na barra. Padrão 'Configurando...'.
    """
    print()
    total = 0
    for value in track(range(100), description=description):
        time.sleep(time_)
        total += 1


def ler_arquivo(env: str) -> List[str]:
    """Verifica se o arquivo de .env existe. Se sim, lê linha por linha.

    Args:
        env (str): Arquivo que será lido.

    Returns:
        list: Retorna uma lista, separando o arquivo por linhas.
    """
    if not os.path.exists(env):
        open(env, 'w').close()

    with open(env, 'r+') as arquivo:
        return arquivo.readlines()


def log_mensagem(tipo: str, mensagem: str) -> None:
    """Armazena os logs e exibe na tela

    Args:
        tipo (str): tipo de log que vai executar (info ou erro).
        mensagem (str): Mensagem que será exibida no log.
    """
    console.log(f'{mensagem}\n')

    match tipo:
        case 'info':
            logger.info(mensagem)
        case 'erro':
            logger.error(mensagem)


def adicionar_credencial(chave: str, valor: List[str], env: str) -> None:
    """Adiciona as credenciais no arquivo de variável de ambiente.

    Args:
        chave (str): Chave da variável a ser criada.
        valor (List[str]): Valor da chave criada. No caso dessa função, uma lista com uma string dentro.
        env (str): Arquivo de variável de ambiente onde será gravada a variável. Padrão settings.ENV.
    """
    linhas = ler_arquivo(env)

    if not any(chave in linha for linha in linhas):
        with open(env, 'a+') as arquivo:
            arquivo.write(f'{chave}="{valor}"\n')
            progress_bar()
            log_mensagem('info', f'{chave} configurada com sucesso.')

    progress_bar(0, description='[b][red]ERRO!!![/red][b]')
    log_mensagem('erro', 'f{chave} já existe no arquivo.')
