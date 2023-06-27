import logging.config

from rocketry import Rocketry

from app.tasks import envia, formata, texto

app = Rocketry()
logging.config.fileConfig('app/config/logging.conf')

app.include_grouper(texto.group)
app.include_grouper(envia.group)
app.include_grouper(formata.group)
