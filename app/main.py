import logging

from rocketry import Rocketry
from rocketry.args import Config

from app.tasks import envia, formata, texto

app = Rocketry(
    config={
        'silence_task_prerun': False,
        'silence_task_logging': False,
        'silence_cond_check': False,
    },
)

app.include_grouper(texto.group)
app.include_grouper(envia.group)
app.include_grouper(formata.group)


handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
task_logger = logging.getLogger('rocketry.task')
task_logger.addHandler(handler)
