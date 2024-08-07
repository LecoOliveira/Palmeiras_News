from rocketry import Rocketry

from app.tasks import envia, formata, texto

app = Rocketry()

app.include_grouper(texto.group)
app.include_grouper(envia.group)
app.include_grouper(formata.group)
