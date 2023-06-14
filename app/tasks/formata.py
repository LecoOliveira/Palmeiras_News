from rocketry import Grouper
from rocketry.args import Return
from rocketry.conds import after_success

from app.tasks.texto import texto_msg

group = Grouper()


@group.task(after_success(texto_msg))
def formata_texto(texto: str = Return(texto_msg)) -> str:
    """
    Formata o texto vindo da função texto_msg().

    Args: Argumentos:
        texto (str): Texto a ser formatado.

    Returns: Retorna:
        str: Texto pronto para ser enviado na função enviar_msg().
    """
    texto = str(texto)

    if texto is not None:
        texto = texto.replace('  ', ' ')
        jogo = texto[: texto.find(' l')]
        campeonato = texto[texto.find(' l') + 2 : texto.find(')') + 1]
        data = texto[texto.find('Data') : texto.find('Local')].replace(
            ' l ', ' '
        )
        local = texto[texto.find('Local') : texto.find('Trans')]
        transmissao = texto[texto.find('Trans') : texto.find('Árb')]
        arbitro = texto[texto.find('Árb') : texto.find('Esca')]
        escalacao = texto[texto.find('Esca') : texto.find('Pend')]
        pendurados = texto[texto.find('Pend') : texto.find('Susp')]
        suspensos = texto[texto.find('Susp') : texto.find('Des')]
        desfalques = texto[texto.find('Desf') :]
        return (
            f'\n{jogo} |{campeonato}\n\n{data}\n'
            f'{local}\n{transmissao}\n{arbitro}\n\n'
            f'{escalacao}\n\n{pendurados}\n\n{suspensos}\n\n{desfalques}'
        )
