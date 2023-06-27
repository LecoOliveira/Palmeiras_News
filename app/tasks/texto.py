from bs4 import BeautifulSoup as bs
from requests import get
from rocketry import Grouper
from rocketry.args import Arg, FuncArg, Return
from rocketry.conds import daily, retry, time_of_day

from app.arguments import hora_jogo, link_jogo
from app.conditions import data_igual
from app.config.constants import HEADERS

group = Grouper()
hora_max = f'{str(int(hora_jogo()[:2]) + 2)}:30'
sem_dados = 'Não há relatos sobre este jogo.'


@group.task(daily.between(f'{hora_jogo}', f'{hora_max}') & data_igual)
def texto_msg(link: str = link_jogo) -> str:
    """
    Função que faz o web scraping no corpo do site e captura o texto que será enviado na mensagem.

    Args: Argumentos:
        link (str): link de onde será buscado o texto. Parâmetro retornado da função link_jogo().

    Returns: Retorna:
        str: Retorna o texto não formatado com os dados da partida.
    """

    texto_final = bs((get(link, headers=HEADERS)).content, 'html.parser').find(
        'div', {'class': 'pretexto'}
    )

    # if texto_final.text.strip('\n') != sem_dados:
    return (
        texto_final.find('p').find('p').get_text('\n').replace('\n', ' ')
        if texto_final.text.strip('\n') != sem_dados
        else sem_dados
    )
