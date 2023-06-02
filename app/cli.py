import os
import typer

from app.main import app

cli = typer.Typer()


def adicionar_linha(chave: str, valor: str):
    """
    Função principal que adiciona os arquivos no arquivo de variável de ambiente.

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
            typer.echo(f'{chave} adicionada com sucesso!')
        else:
            typer.echo(f'{chave} já existente no arquivo.')


@cli.command()
def sid(sid: str):
    """
    Adiciona o SID da conta Twilio na variável de ambiente;
    Usage: palmeiras sid YOUR_TWILIO_SID
    
    Args:
        sid (str): SID da conta na Twilio.

    """
    adicionar_linha('TWILIO_SID', sid)


@cli.command()
def token(token: str):
    """
    Adiciona o TOKEN da conta Twilio na variável de ambiente;
    Usage: palmeiras token YOUR_TWILIO_TOKEN

    Args:
        token (str): TOKEN da conta na Twilio.

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
def destiny_phone(phone: str):
    """
    Adiciona números de destino para onde serão enviadas as mensagens;
    Usage: palmeiras destiny-phone YOUR_TWILIO_DESTINY_PHONE

    Args:
        phone (str): Numero de destino das mensagens (cadastrados previamente no site).

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
            if phone not in numeros_telefone[0]:
                numeros_telefone = f'{numeros_telefone[0]} {phone}'
                with open('teste.txt', 'w') as fw:
                    for linha in linhas:
                        if chave not in linha:
                            fw.write(linha)
                    else:
                        fw.write(f'{chave}="{numeros_telefone}"')
            else:
                typer.echo('O número de telefone já está configurado.')


@cli.command()
def listar(
    destiny_phone: bool = False,
    sid: bool = False,
    twilio_phone: bool = False,
    token: bool = False,
):
    """
    Lista todas as variáveis de ambiente cadastradas.
    Args: --phone, --destiny-phone, --sid, --twilio-phone;
    
    Ex: palmeiras listar --sid
    """

    option = {
        destiny_phone: 'DESTINY_PHONE_NUMBER',
        sid: 'TWILIO_SID',
        twilio_phone: 'TWILIO_PHONE_NUMBER',
        token: 'TWILIO_TOKEN',
    }.get(True, None)

    if option is None:
        typer.echo(
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
                typer.echo(''.join(valores))
            else:
                typer.echo(
                    f'\nNenhuma variável de ambiente "{option}" encontrada.\n'
                    f'Tente: palmeiras [OPTION] [ARG]\n'
                )
    except IOError:
        typer.echo('Erro ao ler o arquivo.')


@cli.command()
def iniciar():
    app.run()

if __name__ == '__main__':
    cli()
