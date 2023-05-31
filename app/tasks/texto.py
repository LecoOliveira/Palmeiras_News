from bs4 import BeautifulSoup as bs
from requests import get
from rocketry import Grouper
from rocketry.args import Arg, FuncArg, Return
from rocketry.conds import daily, retry, time_of_day

from arguments import link_jogo, hora_jogo
from conditions import data_igual
from constants import HEADERS

group = Grouper()
hora_max = f'{str(int(hora_jogo()[:2]) + 1)}:30'

@group.task(
    (daily.at(f'{hora_jogo}') & data_igual | retry(3))
    & time_of_day.between(f'{hora_jogo}', f'{hora_max}')
)
def texto_msg(link: str = link_jogo) -> str:
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
