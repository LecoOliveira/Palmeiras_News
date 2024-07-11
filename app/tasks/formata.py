import logging.config

from rocketry import Grouper
from rocketry.args import Return
from rocketry.conds import after_success

from app.tasks.texto import sem_dados, texto_msg

group = Grouper()
logging.config.fileConfig('app/config/logging.conf')


@group.task(after_success(texto_msg))
def formata_texto(texto: list = Return(texto_msg)) -> str:
    """
    Formata o texto vindo da função texto_msg().

    Args: Argumentos:
        texto (list): Texto a ser formatado dentro de uma lista.

    Returns: Retorna:
        str: Texto pronto para ser enviado na função enviar_msg().
    """

    if texto[0] != sem_dados:
        chaves = [
            texto[indice].strip().strip(':')
            for indice in range(len(texto))
            if not indice % 2
        ]

        valores = [
            frase.replace(' l ', ' | ').strip(': ')
            for frase in texto
            if frase.strip().strip(':') not in chaves
        ]

        dicionario = dict(zip(chaves, valores))

        return '\n\n'.join(
            f'{chave}: {dicionario[chave]}' for chave in dicionario.keys()
        )

    return ''.join(texto)
