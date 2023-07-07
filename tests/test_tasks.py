import os
from datetime import datetime
from unittest import mock

from twilio.base.exceptions import TwilioRestException

from app.tasks.envia import enviar_msg
from app.tasks.formata import formata_texto
from app.tasks.texto import sem_dados, texto_msg

test_link = 'https://www.palmeiras.com.br/jogo/?idjogo=2588'
test_hora_jogo = datetime.now().strftime('%H:%M')

result = texto_msg(test_link)


# texto_msg tests --------------------------------------------------


def test_texto_msg_nao_deve_retornar_None():
    assert result is not None


def test_texto_msg_deve_retornar_algum_texto_em_uma_lista():
    assert isinstance(result, list)


def test_texto_msg_nao_esta_vazio():
    assert len(result) > 0


# enviar_msg tests -------------------------------------------------


@mock.patch('app.tasks.envia.CLIENT.messages.create')
def test_enviar_msg_esta_funcionando(create_message_mock):
    expected_sid = 'SM87105da94bff44b999e4e6eb90d8eb6a'
    create_message_mock.return_value.sid = expected_sid
    message = create_message_mock
    sid = enviar_msg()

    assert create_message_mock.called is True
    assert sid == expected_sid


@mock.patch('app.tasks.envia.CLIENT.messages.create')
def test_enviar_msg_log_error_when_cannot_send_a_message(
    create_message_mock, caplog
):
    error_message = 'Unable to create'
    status = 500
    uri = '/Accounts/ACXXXXXXXXXXXXXXXXX/Messages.json'
    msg = error_message
    create_message_mock.side_effect = TwilioRestException(
        status, uri, msg=error_message
    )

    sid = enviar_msg('Wrong message')

    assert sid is None
    assert 'Erro ao enviar mensagem' in caplog.text
    assert error_message in caplog.text


# formata_texto tests ----------------------------------------------


def test_formata_texto_deve_retronar_um_str():
    assert isinstance(formata_texto(texto=result), str)


def test_formata_texto_deve_retornar_aviso_caso_nao_tenha_dados_do_jogo():
    assert formata_texto(texto=list({sem_dados})) == sem_dados
