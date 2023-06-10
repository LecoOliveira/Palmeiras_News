import logging

from rocketry import Rocketry
from rocketry.args import Config

from app.tasks import envia, formata, texto

app = Rocketry()

app.include_grouper(texto.group)
app.include_grouper(envia.group)
app.include_grouper(formata.group)


handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
task_logger = logging.getLogger('rocketry.task')
task_logger.addHandler(handler)


@app.setup()
def set_config(config=Config()):
    config.silence_task_prerun = False
    config.silence_task_logging = False
    config.silence_cond_check = False


# if __name__ == '__main__':
#     app.run()
