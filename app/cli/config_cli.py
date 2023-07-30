import logging
import logging.config
import os
import time
from typing import List

from rich.console import Console
from rich.progress import track

from app.config.constants import ENV

logging.config.fileConfig('app/config/logging.conf')
logger = logging.getLogger('rocketry.task')
console = Console()


def progress_bar(time_: float = 0.02, description: str = 'Configurando...'):
    print()
    total = 0
    for value in track(range(100), description=description):
        time.sleep(time_)
        total += 1


def ler_arquivo(env: str) -> list:
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


def adicionar_credencial(chave: str, valor: List[str], env: str):
    """Adiciona as credenciais no arquivo de variável de ambiente.

    Args:
        chave (str): Chave da variável a ser criada.
        valor (List[str]): Valor da chave criada. No caso dessa função, uma lista com uma string dentro.
        env (str): Arquivo de variável de ambiente onde será gravada a variável.
    """
    linhas = ler_arquivo(env)
    if not any(chave in linha for linha in linhas):
        with open(env, 'a+') as arquivo:
            arquivo.write(f'{chave}="{valor}"\n')
        progress_bar()
        msg_confirmacao = f'{chave} configurado com sucesso!'
        console.log(f'{msg_confirmacao}\n')
        logger.info(msg_confirmacao)
    else:
        progress_bar(0, description='[b][red]ERRO!!![/red][b]')
        msg_erro = f'{chave} já existe no arquivo.'
        console.log(f'{msg_erro}\n')
        logger.error(msg_erro)


def mensagem_confirmação(phone: str, chave: str):
    """Função que mostra mensagem de confirmação após configurar telefone.

    Args:
        phone (str): Telefone que aparecerá na mensagem de confirmação.
        chave (str): Chave da variável, que se´ra mostrada na mensagem.
    """
    progress_bar()
    msg_confirmacao = f'{chave} {phone} configurado com sucesso.'
    console.log(f'{msg_confirmacao}\n')
    logger.info(msg_confirmacao)


def mensagem_erro(
    phone: str, twilio_phones_list: list, phones_adicionados: list
):
    """Função que mostra mensagem de erro ao configurar destiny-phone.

    Args:
        phone (str): Telefone que aparecerá na mensagem de erro.
        twilio_phones_list (list): Lista onde será pego o telefone.
        phones_adicionados (list): Telefones adicionados.
    """
    if phone in twilio_phones_list and phone not in phones_adicionados:
        progress_bar(0, description='[b][red]ERRO!!![/red][b]')
        msg_erro = f'O telefone {phone} já existe no arquivo.'
        console.log(f'{msg_erro}\n')
        logger.error(msg_erro)


def adicionar_phone(chave: str, valor: List[str], env: str):
    """Adiciona os telefones de destino (destiny_phones) no arquivo de variável de ambiente.

    Args:
        chave (str): Chave da variável a ser criada.
        valor (List[str]): Valor da chave criada.
        env (str): Arquivo de variável de ambiente onde será gravada a variável.
    """
    linhas = ler_arquivo(env)
    encontrado = any(chave in linha for linha in linhas)

    if encontrado:
        for indice, linha in enumerate(linhas):
            if chave in linha:
                linha = linha.rstrip('\n')
                partes_linha = linha.split('"')
                phones_agrupados = partes_linha[1]

                twilio_phones_list = phones_agrupados.split()

                phones_novos = filter(
                    lambda phone: phone not in twilio_phones_list,
                    valor,
                )

                phones_adicionados = [
                    phone
                    for phone in phones_novos
                    if phone not in twilio_phones_list
                ]

                if phones_adicionados:
                    phones_agrupados = ' '.join(
                        twilio_phones_list + phones_adicionados
                    )
                    linha = (
                        f'{partes_linha[0]}"{phones_agrupados}"'
                        f'{partes_linha[2]}\n'
                    )
                    linhas[indice] = linha

                list(
                    map(
                        lambda phone: mensagem_confirmação(phone, chave),
                        phones_adicionados,
                    )
                )

                list(
                    map(
                        lambda phone: mensagem_erro(
                            phone, twilio_phones_list, phones_adicionados
                        ),
                        valor,
                    )
                )

                with open(env, 'w') as arquivo:
                    arquivo.writelines(linhas)
                return

    with open(env, 'a+') as arquivo:
        arquivo.write(f'{chave}="{" ".join(valor)}"\n')
    progress_bar()
    msg_confirmacao = f'{chave} {" ".join(valor)} configurado(s) com sucesso.'
    console.log(f'{msg_confirmacao}\n')
    logger.info(msg_confirmacao)


def adicionar_linha(chave: str, valor: List[str], env: str = ENV):
    """Função que adiciona a linha no arquivo.

    Args:
        chave (str): Chave da variável de ambiente.
        valor (List): Valor da variável de ambiente.
        env (str, optional): Arquivo de variável de ambiente. Padrão: .env
    """
    if chave != 'TWILIO_DESTINY_PHONE_NUMBER':
        adicionar_credencial(chave, valor, env)
    else:
        adicionar_phone(chave, valor, env)
