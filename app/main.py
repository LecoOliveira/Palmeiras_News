import os
from datetime import datetime
from re import compile

from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
from functions import *
from requests import get
from rocketry import Rocketry
from rocketry.args import Arg, Return
from rocketry.conds import (
    after_fail,
    after_finish,
    after_success,
    daily,
    minutely,
    retry,
    time_of_day,
)
from twilio.rest import Client

app = Rocketry()


@app.param('data')
def data_hoje() -> str:
    """
    Função que usa a biblioteca 'datetime' para buscar a data do dia.

    Returns:
        str: Retorna a data do dia, no formato 'dd/mm'.
    """
    return datetime.today().strftime('%d/%m')


@app.param('data_jogo')
def data_jogo() -> str:
    """
    Busca a data do próximo jogo dentro do site.

    Returns:
        str: Retorna a data no formato: 'dd/mm'
    """

    html_principal = bs(
        (get(URL_PRINCIPAL, headers=HEADERS)).content, 'html.parser'
    )

    return (
        html_principal.find('div', class_='faixa')
        .find('div', {'class': 'header-tempo-real-campeonato'})
        .find_all('span', string=compile('/'))[0]
        .text
    )


@app.param('link')
def link_jogo() -> str:
    """
    Faz a raspagem no site para encontrar o link da próxima partida.

    Returns:
        str: Retorna o link do próximo jogo.
    """

    html_principal = bs(
        (get(URL_PRINCIPAL, headers=HEADERS)).content, 'html.parser'
    )

    return (
        bs((get(URL_PRINCIPAL, headers=HEADERS)).content, 'html.parser')
        .find('div', class_='faixa')
        .find('a')
        .get('href')
    )


@app.cond()
def data_igual(
    data: str = Arg('data'), data_jogo: str = Arg('data_jogo')
) -> bool:
    """
    Função que se torna uma condição através da biblioteca 'Rocketry',
    a saída dela determina se a próxima função roda ou não dentro das nossas tarefas.

    Args:
        data (str): Dia atual. Parâmetro retornado de Arg('data').
        data_jogo (str): Data do próximo jogo. Parâmetro retornado de Arg('data_jogo').

    Returns:
        bool: True ou False
    """
    return False if data != data_jogo else True


@app.task(
    (daily.at('12:00') & data_igual | retry(3))
    & time_of_day.between('12:00', '14:00')
)
def texto_msg(link: str = Arg('link')) -> str:
    """
    Função que faz o webscraping no corpo do site.

    Args:
        link (str): link de onde será buscado o texto. Parâmetro retornado de Arg('link').

    Returns:
        str: Retorna o texto não formatado com os dados da partida.
    """

    texto_final = (
        bs((get(link, headers=HEADERS)).content, 'html.parser')
        .find('div', {'class': 'pretexto'})
        .text.strip('\n')
    )

    if texto_final != 'Não há relatos sobre este jogo.':
        return (
            bs((get(link, headers=HEADERS)).content, 'html.parser')
            .find('div', {'class': 'pretexto'})
            .find('p')
            .find('p')
            .get_text('\n')
            .replace('\n', ' ')
        )


@app.task(after_success(texto_msg))
def formata_texto(texto: str = Return(texto_msg)) -> str:
    """
    Formata o texto vindo da função 'texto_msg()'

    Args:
        texto (str): Texto a ser formatado retornado de: Return(texto_msg).

    Returns:
        str: Texto pronto para ser enviado na função 'enviar_msg()'.
    """

    texto = texto.replace('  ', ' ')
    jogo = texto[: texto.find(' l')]
    campeonato = texto[texto.find(' l') + 2 : texto.find(')') + 1]
    data = texto[texto.find('Data') : texto.find('Local')].replace(' l ', ' ')
    local = texto[texto.find('Local') : texto.find('Trans')]
    transmissao = texto[texto.find('Trans') : texto.find('Árb')]
    arbitro = texto[texto.find('Árb') : texto.find('Esca')]
    escalacao = texto[texto.find('Esca') : texto.find('Pend')]
    pendurados = texto[texto.find('Pend') : texto.find('Susp')]
    suspensos = texto[texto.find('Susp') : texto.find('Retor')]
    desfalques = texto[texto.find('Desf') :]
    return (
        f'\n{jogo} |{campeonato}\n\n{data}\n'
        f'{local}\n{transmissao}\n{arbitro}\n\n'
        f'{escalacao}\n{pendurados}\n{suspensos}\n{desfalques}'
    )


@app.task(after_finish(formata_texto))
def enviar_msg(texto: str = Return(formata_texto)) -> str:
    """Envia a mensagem para o destino definido em 'destiny_phone_number'

    Args:
        texto (str): Texto ja formatado e pronto para envio.
        Retornado de Return(formata_texto).

    Returns:
        str: Mensagem de confirmação ou de erro.
    """
    load_dotenv('/home/alex/Documentos/Estudos/Palmeiras_News/app/twilio.env')
    ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
    DESTINY_PHONE_NUMBER = os.environ['TWILIO_DESTINY_PHONE_NUMBER']
    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
    return CLIENT.messages.create(
        body=texto, from_=PHONE_NUMBER, to=DESTINY_PHONE_NUMBER
    )


@app.task(after_fail(texto_msg))
def falha():
    print('falha')


app.run()
