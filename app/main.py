import logging

from redbird.logging import RepoHandler
from redbird.repos import CSVFileRepo
from rocketry import Rocketry
from rocketry.args import Config
from rocketry.log import MinimalRecord

from app.tasks import envia, formata, texto

repo = CSVFileRepo(filename='app/task.csv', model=MinimalRecord)

task_logger = logging.getLogger('rocketry.task')
handler = RepoHandler(repo=repo)
task_logger.addHandler(handler)

app = Rocketry(
    config={
        # 'force_status_from_logs': False,
        'silence_task_prerun': False,
        'silence_task_logging': False,
        'silence_cond_check': False,
    },
)

app.include_grouper(texto.group)
app.include_grouper(envia.group)
app.include_grouper(formata.group)


# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# task_logger = logging.getLogger('rocketry.task')
# task_logger.addHandler(handler)

