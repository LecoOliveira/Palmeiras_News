import re

from functions import *

my_regex = re.compile('../..')


def test_data_jogo_retorna_uma_data():
    assert my_regex.match(data_jogo())


def test_texto_msg_nao_deve_retornar_None():
    assert texto_msg() is not None


def test_texto_msg_deve_retornar_algum_texto():
    assert type(texto_msg()) is str
