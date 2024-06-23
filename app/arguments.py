import cloudscraper
from datetime import datetime
from re import compile

from bs4 import BeautifulSoup as bs
from rocketry.args import argument

from app.config.constants import HEADERS, URL_PRINCIPAL

scraper = cloudscraper.create_scraper()

html_principal = bs(
    (scraper.get(URL_PRINCIPAL, headers=HEADERS)).content, 'html.parser'
)


@argument()
def data_hoje() -> str:
    """
    Função que usa a biblioteca 'datetime' para buscar a data do dia.

    Returns:
        str: Retorna a data do dia, no formato 'dd/mm'.
    """
    return datetime.today().strftime('%d/%m')


@argument()
def data_jogo() -> str:
    """
    Busca a data do próximo jogo dentro do site.

    Returns:
        str: Retorna a data no formato: 'dd/mm'
    """

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

    return html_principal.find('div', class_='faixa').find('a').get('href')


@argument()
def hora_jogo() -> str:
    """
    Busca a hora do próximo jogo dentro do site.

    Returns:
        str: Retorna a hora no formato: 'dd/mm'
    """

    hora_jogo = (
        html_principal.find('div', class_='faixa')
        .find('div', {'class': 'header-tempo-real-campeonato'})
        .find(string=compile('..H..'))
        .strip()
        .replace('\n', '')
        .replace('|', '')
        .replace('H',':')
    )

    return hora_jogo
