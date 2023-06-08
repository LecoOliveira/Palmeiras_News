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


@group.task(after_finish(formata_texto))
def enviar_msg(texto: str = Return(formata_texto)) -> str:
    """
    Envia a mensagem para o destino definido em 'destiny_phone_number'

    Args:
        texto (str): Texto ja formatado e pronto para envio. Retornado de Return(formata_texto).

    Returns:
        str: Mensagem de confirmação ou de erro.
    """
    phones = getenv('TWILIO_DESTINY_PHONE_NUMBER').split(' ')
    ACCOUNT_SID = getenv('TWILIO_ACCOUNT_SID')
    AUTH_TOKEN = getenv('TWILIO_AUTH_TOKEN')
    PHONE_NUMBER = getenv('TWILIO_PHONE_NUMBER')
    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

    try:
        for destiny_phone in phones:
            message = CLIENT.messages.create(
                body=texto, from_=PHONE_NUMBER, to=destiny_phone
            )
            print(message.sid)

    except TwilioRestException as erro:
        print(erro)
