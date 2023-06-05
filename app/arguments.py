from datetime import datetime
from re import compile

from bs4 import BeautifulSoup as bs
from requests import get
from rocketry.args import argument

from app.constants import HEADERS, URL_PRINCIPAL


@argument()
def data_hoje() -> str:
    """
    Função que usa a biblioteca 'datetime' para buscar a data do dia.

    Returns:
        str: Retorna a data do dia, no formato 'dd/mm'.
    """
    # return datetime.today().strftime('%d/%m')
    return '04/06'


@argument()
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


@argument()
def link_jogo() -> str:
    """
    Faz a raspagem no site para encontrar o link da próxima partida.

    Returns:
        str: Retorna o link do próximo jogo.
    """

    # html_principal = bs(
    #     (get(URL_PRINCIPAL, headers=HEADERS)).content, 'html.parser'
    # )

    # return html_principal.find('div', class_='faixa').find('a').get('href')
    return 'https://www.palmeiras.com.br/jogo/?idjogo=2588'


@argument()
def hora_jogo():
    """
    Busca a hora do próximo jogo dentro do site.

    Returns:
        str: Retorna a hora no formato: 'dd/mm'
    """

    # html_principal = bs(
    #     (get(URL_PRINCIPAL, headers=HEADERS)).content, 'html.parser'
    # )

    # hora_jogo = (
    #     html_principal.find('div', class_='faixa')
    #     .find('div', {'class': 'header-tempo-real-campeonato'})
    #     .find(string=compile('..H..'))
    #     .strip()
    #     .replace('\n', '')
    #     .replace('|', '')
    # )

    # return f'{str(int(hora_jogo[:2]) - 2)}:00'
    return '16:44'
