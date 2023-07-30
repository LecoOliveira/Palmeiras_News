import logging
import logging.config

from rocketry import Grouper
from rocketry.args import Return
from rocketry.conds import after_finish
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from app.config.twilio import ACCOUNT_SID, AUTH_TOKEN, PHONE_NUMBER, phones
from app.tasks.formata import formata_texto

group = Grouper()
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
logging.config.fileConfig('app/config/logging.conf')
logger = logging.getLogger('rocketry.task')


@group.task(after_finish(formata_texto))
def enviar_msg(texto: str = Return(formata_texto)) -> str:
    """
    Envia a mensagem para os números configurados no arquivo de variável de ambiente.

    Args: Argumentos:
        texto (str): Texto ja formatado e pronto para envio. Texto de retorno da função formata_texto().

    Returns: Retorna:
        str: Mensagem de confirmação ou de erro.
    """
    try:
        for destiny_phone in phones:
            message = CLIENT.messages.create(
                body=texto, from_=PHONE_NUMBER, to=destiny_phone
            )

    except TwilioRestException as erro:
        logger.error('Erro ao enviar mensagem! (Unable to create...)')
        return

    return message.sid
