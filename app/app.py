import os
from datetime import datetime

from functions import *

# Coleta a data do sistema ja fomatada.
data_hoje = datetime.today().strftime('%d/%m')


# if data_hoje == data_jogo() or (int(data_hoje[:2]) + 1) == int(
#     data_jogo()[:2]
# ):
#     enviar_msg()
print(data_jogo())
