import re

from rocketry.conds import false, true

from app.arguments import *
from app.conditions import data_igual
from app.tasks.texto import texto_msg

my_regex = re.compile('../..')
link = link_jogo()


def test_data_jogo_retorna_uma_data():
    assert my_regex.match(data_jogo())


def test_texto_msg_nao_deve_retornar_None():
    assert texto_msg(link) is not None


def test_texto_msg_deve_retornar_algum_texto():
    assert type(texto_msg(link)) is str


def test_data_igual_deve_retornar_false_ou_true():
    cond = data_igual()
    assert cond.observe() == True or cond.observe() == False


def test_data_igual_deve_retornar_false():
    cond = data_igual()
    if data_hoje() != data_jogo():
        assert cond.observe() == False


def test_data_igual_deve_retornar_true():
    cond = data_igual()
    if data_hoje() == data_jogo():
        assert cond.observe() == True
