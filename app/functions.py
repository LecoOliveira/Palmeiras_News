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


def data_jogo() -> str:
    """
    Busca a data do próximo jogo dentro do site.

    Returns:
        str: Retorna a data do próximo jogo no formato: 'dd/mm'

    Examples:
        >>> data_jogo()
        '24/05'

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


def enviar_msg() -> str:
    """Envia a mensagem para o destino definido em 'destiny_phone_number'

    Returns:
        str: Mensagem de confirmação ou de erro.
    """
    # Credenciais da conta Twilio, armazenadas em uma variável de ambiente.
    # Para mais informações: https://www.twilio.com/docs/usage/secure-credentials
    #                        https://www.twilio.com/blog/environment-variables-python
    load_dotenv('/home/alex/Documentos/Estudos/Palmeiras_News/app/twilio.env')
    ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
    DESTINY_PHONE_NUMBER = os.environ['TWILIO_DESTINY_PHONE_NUMBER']
    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

    if texto_msg() != 'Não há relatos sobre este jogo.':
        return CLIENT.messages.create(
            body=texto_msg(), from_=PHONE_NUMBER, to=DESTINY_PHONE_NUMBER
        )
