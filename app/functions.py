import os
from re import compile

from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
from requests import get
from twilio.rest import Client

URL_PRINCIPAL = 'https://www.palmeiras.com.br/home/'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}


def enviar_msg(texto: str) -> str:
    """Envia a mensagem para o destino definido em 'destiny_phone_number'

    Args:
        texto (str): Texto ja formatado para envio.

    Returns:
        str: Mensagem de confirmação ou de erro.
    """
    load_dotenv('/home/alex/Documentos/Estudos/Palmeiras_News/app/twilio.env')
    ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
    DESTINY_PHONE_NUMBER = os.environ['TWILIO_DESTINY_PHONE_NUMBER']
    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

    if texto != 'Não há relatos sobre este jogo.':
        return CLIENT.messages.create(
            body=texto, from_=PHONE_NUMBER, to=DESTINY_PHONE_NUMBER
        )


def link_jogo() -> str:
    """Faz a raspagem no site para encontrar o link da próxima partida.

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


def texto_msg(link: str) -> str:
    """Função que faz o webscraping no corpo do site.

    Args:
        str: link de onde será buscado o texto.

    Returns:
        str: Retorna o texto ja formatado com os dados da partida.
    """

    texto_final = (
        bs((get(link, headers=HEADERS)).content, 'html.parser')
        .find('div', {'class': 'pretexto'})
        .text.strip('\n')
    )

    if texto_final == 'Não há relatos sobre este jogo.':
        return texto_final
    else:
        return (
            bs((get(link, headers=HEADERS)).content, 'html.parser')
            .find('div', {'class': 'pretexto'})
            .find('p')
            .find('p')
            .get_text('\n')
            .replace('\n', ' ')
        )


def formata_texto(texto: str) -> str:
    """Formata o texto vindo da função 'texto_msg()'

    Args:
        texto (str): Texto a ser formatado

    Returns:
        str: Texto pronto para ser enviado na função 'enviar_msg()'
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
        f'\n{jogo} |{campeonato}\n{data}\n'
        f'{local}\n{transmissao}\n{arbitro}\n'
        f'{escalacao}\n{pendurados}\n{suspensos}\n{desfalques}'
    )
