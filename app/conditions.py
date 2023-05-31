from rocketry.conds import condition

from arguments import data_hoje, data_jogo


@condition()
def data_igual(
    data: str = data_hoje, data_jogo: str = data_jogo
) -> bool:
    """
    Função que se torna uma condição através da biblioteca 'Rocketry',
    a saída dela determina se a próxima função roda ou não dentro das nossas tarefas.

    Args:
        data (str): Dia atual. Parâmetro importado de ```app_teste.arguments.data_hoje```.
        data_jogo (str): Data do próximo jogo. Parâmetro importado de ```app_teste.arguments.data_hoje```.

    Returns:
        bool: True ou False
    """
    return False if data != data_jogo else True
