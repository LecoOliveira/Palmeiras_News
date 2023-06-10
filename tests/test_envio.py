from unittest import mock

from app.tasks.envia import enviar_msg


@mock.patch('app.tasks.envia.CLIENT.messages.create')
def test_enviar_msg_esta_funcionando(create_message_mock):
    expected_sid = 'SM87105da94bff44b999e4e6eb90d8eb6a'
    create_message_mock.return_value.sid = expected_sid
    message = create_message_mock
    sid = enviar_msg()

    assert create_message_mock.called is True
    assert sid == expected_sid
