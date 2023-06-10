from unittest import mock

from app.tasks.envia import enviar_msg


@mock.patch('app.tasks.envia.CLIENT.messages.create')
def test_enviar_msg_esta_funcionando(create_message_mock):
    message = 'oi'
    expected_sid = 'SM87105da94bff44b999e4e6eb90d8eb6a'
    create_message_mock.return_value.sid = expected_sid
    sid = enviar_msg(message)

    assert create_message_mock.called is True
