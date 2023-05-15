from bs4 import BeautifulSoup as bs
from requests import get
from re import compile


url_principal = 'https://www.palmeiras.com.br/home/'

# Headers para usar caso necessário uma "autenticação". Não obrigatório.
headers = {
    'User-Agent':
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
}


# Encontra a data do próximo jogo.
def data_jogo() -> str:

    html_principal = bs(
        (get(url_principal, headers=headers)).content, 'html.parser')

    return html_principal.find(
        'div', class_='faixa').find(
        'div', {'class': 'header-tempo-real-campeonato'}).find_all(
        'span', string=compile('/'))[0].text


# Encontra o texto da mensagem.
def texto_msg() -> str:

    html_principal = bs(
        (get(url_principal, headers=headers)).content, 'html.parser')

    link_jogo = html_principal.find(
        'div', class_='faixa').find('a').get('href')

    html_jogo = bs((get(link_jogo, headers=headers)).content, 'html.parser')

    texto_final = html_jogo.find('div', {'class': 'pretexto'}).text.strip('\n')

    if texto_final == 'Não há relatos sobre este jogo.':
        return texto_final
    else:
        return html_jogo.find('div', {'class': 'pretexto'}).find('p').find('p').text
