from datetime import datetime

from app.tasks.texto import texto_msg

test_link = 'https://www.palmeiras.com.br/jogo/?idjogo=2588'
test_hora_jogo = datetime.now().strftime('%H:%M')

result = texto_msg(test_link)


def test_texto_msg_nao_deve_retornar_None():
    assert result is not None


def test_texto_msg_deve_retornar_algum_texto():
    assert isinstance(result, str)


def test_texto_msg_nao_esta_vazio():
    assert len(result) > 0
