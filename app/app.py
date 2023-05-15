import os
from datetime import datetime

from dotenv import load_dotenv
from functions import data_jogo, texto_msg
from twilio.rest import Client

# Credenciais da conta Twilio, armazenadas em uma variável de ambiente.
# Para mais informações: https://www.twilio.com/docs/usage/secure-credentials
#                        https://www.twilio.com/blog/environment-variables-python
load_dotenv('/home/alex/Documentos/Estudos/Palmeiras_News/app/twilio.env')
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
phone_number = os.environ['TWILIO_PHONE_NUMBER']
client = Client(account_sid, auth_token)


# Coleta a data do sistema e formata.
data_hoje = datetime.today().strftime('%d/%m')


def enviar_msg():
    return client.messages.create(
        body=texto_msg(), from_=phone_number, to='+5511940228960'
    )


if data_hoje == data_jogo() or (int(data_hoje[:2]) + 1) == int(
    data_jogo()[:2]
):
    enviar_msg()
