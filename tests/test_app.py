from re import compile

from app.arguments import *
from app.conditions import data_igual

data_regex = compile('../..')
link_regex = compile('https://')
link_teste = 'https://www.palmeiras.com.br/jogo/?idjogo=2588'
data_teste = '31/02'


def test_link_jogo_deve_começar_com_http():
    assert link_regex.match(link_jogo())


def test_data_jogo_retorna_uma_data():
    assert data_regex.match(data_jogo())


def test_data_igual_deve_retornar_um_dado_booleano():
    cond = data_igual()
    assert isinstance(cond.observe(), bool)


def test_data_igual_deve_retornar_false_ou_true_dependendo_do_data_igual():
    cond = data_igual()
    assert cond.observe() == False if data_hoje() != data_jogo() else True
