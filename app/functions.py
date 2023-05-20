from re import compile

from bs4 import BeautifulSoup as bs
from requests import get

URL_PRINCIPAL = 'https://www.palmeiras.com.br/home/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}


def data_jogo() -> str:
    """Busca a data do próximo jogo dentro do site.

    Returns:
        str: 'dd/mm'
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


# Encontra o texto da mensagem.
def texto_msg() -> str:
    """Função que faz o webscraping no corpo do site.

    Returns:
        str: Retorna o texto ja formatado com os dados da partida.
    """

    html_principal = bs(
        (get(URL_PRINCIPAL, headers=HEADERS)).content, 'html.parser'
    )

    link_jogo = (
        bs((get(URL_PRINCIPAL, headers=HEADERS)).content, 'html.parser')
        .find('div', class_='faixa')
        .find('a')
        .get('href')
    )

    texto_final = (
        bs((get(link_jogo, headers=HEADERS)).content, 'html.parser')
        .find('div', {'class': 'pretexto'})
        .text.strip('\n')
    )

    if texto_final == 'Não há relatos sobre este jogo.':
        return texto_final
    else:
        return (
            bs((get(link_jogo, headers=HEADERS)).content, 'html.parser')
            .find('div', {'class': 'pretexto'})
            .find('p')
            .find('p')
            .get_text('\n')
            .replace('\n', '\n\n')
        )
