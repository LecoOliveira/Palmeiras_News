import os
from datetime import datetime

from functions import *

# Coleta a data do sistema ja fomatada.
data_hoje = datetime.today().strftime('%d/%m')


# if data_hoje == data_jogo() or (int(data_hoje[:2]) + 1) == int(
#     data_jogo()[:2]
# ):
#     enviar_msg()
link = 'https://www.palmeiras.com.br/jogo/?idjogo=2587'
texto = texto_msg(link)
print(formata_texto(texto))
