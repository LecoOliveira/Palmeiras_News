import os
import subprocess
from typing import List

import typer
from rich.console import Console

from app.main import app

cli = typer.Typer(help='Inerface para adição de variáveis de ambiente.')
console = Console()


def adicionar_linha(chave: str, valor: str):
    """
    Função principal que adiciona os dados no arquivo de variável de ambiente.

    Args:
        chave (str): Recebe a chave da variável a ser criada.
        valor (str): Recebe o valor da chave criada.
    Ex:
        O resultado final ficará assim:
        ```CHAVE_DA_VARIAVEL="valor_da_variavel"```
    """
    if not os.path.exists('teste.txt'):
        with open('teste.txt', 'w') as arq:
            arquivo = arq.write(' ')
    with open('teste.txt', 'r+') as arquivo:
        linhas = arquivo.readlines()
        if not any(chave in linha for linha in linhas):
            arquivo.write(f'\n{chave}="{valor}"')
            console.log(f'{chave} adicionada com sucesso!')
        else:
            console.log(f'{chave} já existente no arquivo.')


@cli.command()
def sid(sid: str):
    """
    Adiciona o SID da conta Twilio na variável de ambiente;
    Usage: palmeiras sid YOUR_TWILIO_SID

    Args:
        sid (str): SID disponibilizado pela Twilio ao criar a sua conta.
    """
    adicionar_linha('TWILIO_SID', sid)


@cli.command()
def token(token: str):
    """
    Adiciona o TOKEN da conta Twilio na variável de ambiente;
    Usage: palmeiras token YOUR_TWILIO_TOKEN

    Args:
        token (str): TOKEN disponibilizado pela Twilio ao criar a sua conta.
    """
    adicionar_linha('TWILIO_TOKEN', token)


@cli.command()
def twilio_phone(phone: str):
    """
    Adiciona o seu PHONE_NUMBER da conta Twilio na variável de ambiente;
    Usage: palmeiras twilio-phone YOUR_TWILIO_PHONE

    Args:
        phone (str): Telefone gerado pela conta Twilio.
    """
    adicionar_linha('TWILIO_PHONE_NUMBER', phone)


@cli.command()
def destiny_phone(phones: List[str]):
    """
    Adiciona números de destino para onde serão enviadas as mensagens;
    Usage: palmeiras destiny-phone YOUR_TWILIO_DESTINY_PHONES (Separados por espaço)

    Args:
        phone (str): Número de destino das mensagens (cadastrados previamente no site).
    """
    chave = 'DESTINY_PHONE_NUMBER'
    if not os.path.exists('teste.txt'):
        with open('teste.txt', 'w') as arq:
            arquivo = arq.write(' ')

    with open('teste.txt', 'r+') as fr:
        linhas = fr.readlines()
        if not any(chave in linha for linha in linhas):
            adicionar_linha(chave, phone)

        else:
            numeros_telefone = [
                linha.split('=')[1].replace('"', '').strip()
                for linha in linhas
                if chave in linha
            ]
            for phone in phones:
                if phone not in numeros_telefone[0]:
                    numeros_telefone = f'{numeros_telefone[0]} {phone}'
                    with open('teste.txt', 'w') as fw:
                        for linha in linhas:
                            if chave not in linha:
                                fw.write(linha)
                        else:
                            fw.write(f'{chave}="{numeros_telefone}"')
                            console.log(
                                f'O número {phone} foi adicionada com sucesso!'
                            )

                else:
                    console.log(f'O número {phone} já está configurado.')


@cli.command('show')
def listar(
    destiny_phone: bool = False,
    sid: bool = False,
    twilio_phone: bool = False,
    token: bool = False,
):
    """
    Lista todas as variáveis de ambiente cadastradas.
    Args: --phone, --destiny-phone, --sid, --twilio-phone;

    Ex: palmeiras show --sid
    """

    option = {
        destiny_phone: 'DESTINY_PHONE_NUMBER',
        sid: 'TWILIO_SID',
        twilio_phone: 'TWILIO_PHONE_NUMBER',
        token: 'TWILIO_TOKEN',
    }.get(True, None)

    if option is None:
        console.log(
            '\nNenhuma opção selecionada. Por favor, '
            'escolha uma das opções:\n --twilio-phone, '
            '--destiny-phone, --sid ou --token.\n'
        )
        return

    try:
        with open('teste.txt', 'r') as fr:
            linhas = fr.readlines()
            valores = [linha for linha in linhas if option in linha]
            if valores:
                console.log(''.join(valores))
            else:
                console.log(
                    f'\nNenhuma variável de ambiente "{option}" encontrada.\n'
                    f'Tente: palmeiras [OPTION] [ARG]\n'
                )
    except IOError:
        console.log('Erro ao ler o arquivo.')


@cli.command()
def delete(variavel: str):
    """
    Exclui uma das configurações do arquivo de variável de ambiente.
    Ex: palmeiras delete sid
    Args:
        variavel (str): Variável que deseja apagar.
    """
    option = {
        'destiny_phone' : 'DESTINY_PHONE_NUMBER',
        'sid' : 'TWILIO_SID',
        'twilio_phone' : 'TWILIO_PHONE_NUMBER',
        'token' : 'TWILIO_TOKEN',
    }
    variaveis = open('teste.txt').read().split('\n')
    for i, item in enumerate(variaveis):            
        if option[variavel] in variaveis[i]:
            variaveis.remove(item)
            console.log(f'{option[variavel]} removido com sucesso.')
            return
    else:   
        console.log(f'O arquivo não contém nenhum {option[variavel]}.')
    open('teste.txt', 'w').write('\n'.join(variaveis))


@cli.command()
def iniciar():
    app.run()


if __name__ == '__main__':
    cli()
