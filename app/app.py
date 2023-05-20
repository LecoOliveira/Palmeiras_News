import os
from datetime import datetime

from dotenv import load_dotenv
from functions import data_jogo, texto_msg
from twilio.rest import Client

# Credenciais da conta Twilio, armazenadas em uma variável de ambiente.
# Para mais informações: https://www.twilio.com/docs/usage/secure-credentials
#                        https://www.twilio.com/blog/environment-variables-python
load_dotenv('/home/alex/Documentos/Estudos/Palmeiras_News/app/twilio.env')
ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
PHONE_NUMBER = os.environ['TWILIO_PHONE_NUMBER']
DESTINY_PHONE_NUMBER = os.environ['TWILIO_DESTINY_PHONE_NUMBER']
CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)


# Coleta a data do sistema ja fomatada.
data_hoje = datetime.today().strftime('%d/%m')


def enviar_msg() -> str:
    """Envia a mensagem para o destino definido em 'destiny_phone_number'

    Returns:
        str: Mensagem de confirmação ou de erro.
    """

    if texto_msg() != 'Não há relatos sobre este jogo.':
        return CLIENT.messages.create(
            body=texto_msg(), from_=PHONE_NUMBER, to=DESTINY_PHONE_NUMBER
        )


# if data_hoje == data_jogo() or (int(data_hoje[:2]) + 1) == int(
#     data_jogo()[:2]
# ):
#     enviar_msg()
print(texto_msg())
