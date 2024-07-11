import logging.config

import cloudscraper
from bs4 import BeautifulSoup as bs
from rocketry import Grouper
from rocketry.conds import daily, retry

from app.arguments import hora_jogo, link_jogo
from app.conditions import data_igual
from app.config.settings import Settings

group = Grouper()
settings = Settings()
hora_min = f'{str(int(hora_jogo()[:2]) - 1)}:30'
sem_dados = 'Não há relatos sobre este jogo.'
logging.config.fileConfig('app/config/logging.conf')
scraper = cloudscraper.create_scraper()


@group.task(daily.between(f'{hora_min}', f'{hora_jogo}') & data_igual)
def texto_msg(link: str = link_jogo) -> list:
    """
    Função que faz o web scraping no corpo do site e captura o texto que será enviado na mensagem.

    Args: Argumentos:
        link (str): link de onde será buscado o texto. Parâmetro retornado da função link_jogo().

    Returns: Retorna:
        list: Retorna o texto não formatado com os dados da partida em uma lista.
    """

    text_final = bs(
        (scraper.get(link, headers=settings.HEADERS)).content, 'html.parser'
    ).find('div', {'class': 'pretexto'})

    return (
        list(text_final.p.p.strings)
        if text_final.text.strip('\n') != sem_dados
        else list({sem_dados})
    )
