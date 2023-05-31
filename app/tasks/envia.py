import os

from dotenv import load_dotenv
from rocketry import Grouper
from rocketry.args import Return
from rocketry.conds import after_finish
from twilio.rest import Client


from tasks.formata import formata_texto


group = Grouper()


@group.task(after_finish(formata_texto))
def enviar_msg(texto: str = Return(formata_texto)) -> str:
    """
    Envia a mensagem para o destino definido em 'destiny_phone_number'

    Args:
        texto (str): Texto ja formatado e pronto para envio. Retornado de Return(formata_texto).

    Returns:
        str: Mensagem de confirmação ou de erro.
    """
    load_dotenv('/home/alex/Documentos/Estudos/Palmeiras_News/app/twilio.env')
    phones = os.environ['TWILIO_DESTINY_PHONE_NUMBER'].split(' ')
    ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
    AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
    PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
    CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

    for destiny_phone in phones:
        message = CLIENT.messages.create(
            body=texto, from_=PHONE_NUMBER, to=destiny_phone
        )
        print(message.sid)