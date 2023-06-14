import logging
from os import getenv

from dotenv import load_dotenv
from rocketry import Grouper
from rocketry.args import Return
from rocketry.conds import after_finish
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from app.tasks.formata import formata_texto

group = Grouper()
load_dotenv()

phones = getenv('TWILIO_DESTINY_PHONE_NUMBER').split(' ')
ACCOUNT_SID = getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = getenv('TWILIO_PHONE_NUMBER')
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)


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
        logging.error(f'Oh no: {erro}')
        return

    return message.sid
