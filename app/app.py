from datetime import datetime

from functions import *

# Coleta a data do sistema ja formatada.
data_hoje = datetime.today().strftime('%d/%m')


# if data_hoje == data_jogo() or (int(data_hoje[:2]) + 1) == int(
#     data_jogo()[:2]
# ):
#     enviar_msg()
link = 'https://www.palmeiras.com.br/jogo/?idjogo=2587'
texto = formata_texto(texto_msg(link))
