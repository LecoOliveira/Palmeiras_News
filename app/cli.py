import os
import subprocess
import time
from typing import List

import typer
from rich.console import Console
from rich.progress import track
from typing_extensions import Annotated

cli = typer.Typer(help='Interface para adição de variáveis de ambiente.')
console = Console()
env = '.env'


def progress_bar(time_: int = 0.02):
    total = 0
    for value in track(range(100), description="Configurando..."):
        time.sleep(time_)
        total += 1


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
    if not os.path.exists(env):
        with open(env, 'w+') as arq:
            arquivo = arq.write('')
    with open(env, 'r+') as arquivo:
        linhas = arquivo.readlines()
        if not any(chave in linha for linha in linhas):
            arquivo.write(f'{chave}="{valor}"\n')
            print()
            progress_bar()
            console.log(f'{chave} adicionada com sucesso!\n')
        else:
            print()
            progress_bar(0.001)
            console.log(f'{chave} já existe no arquivo.\n')


@cli.command()
def sid(
    sid: Annotated[
        str,
        typer.Argument(
            help='Seu SID gerado ao efetuar cadastro na Twilio',
            show_default=False,
        ),
    ]
):
    """
    Adiciona o SID da conta Twilio na variável de ambiente;

    Usage: palmeiras sid YOUR_TWILIO_ACCOUNT_SID
    """
    adicionar_linha('TWILIO_ACCOUNT_SID', sid)


@cli.command()
def token(
    token: Annotated[
        str,
        typer.Argument(
            help='Token gerado ao efetuar cadastro na Twilio',
            show_default=False,
        ),
    ]
):
    """
    Adiciona o TOKEN da conta Twilio na variável de ambiente;

    Usage: palmeiras token YOUR_TWILIO_AUTH_TOKEN
    """
    adicionar_linha('TWILIO_AUTH_TOKEN', token)


@cli.command()
def twilio_phone(
    phone: Annotated[
        str,
        typer.Argument(
            help='Número americano gerado pela Twilio',
            show_default=False,
        ),
    ]
):
    """
    Adiciona o seu PHONE_NUMBER da conta Twilio na variável de ambiente;

    Usage: palmeiras twilio-phone YOUR_TWILIO_PHONE
    """
    adicionar_linha('TWILIO_PHONE_NUMBER', phone)


@cli.command()
def destiny_phone(
    phones: Annotated[
        List[str],
        typer.Argument(
            help='Um ou mais lista_phones que deseja configurar '
            '(números devem ser separados por espaço); '
            'Ex: +551199999999 +5511999999999',
            show_default=False,
        ),
    ]
):
    """
    Adiciona números de destino para onde serão enviadas as mensagens;

    Usage: palmeiras destiny-phone YOUR_TWILIO_DESTINY_PHONES
    """
    chave = 'TWILIO_DESTINY_PHONE_NUMBER'
    if not os.path.exists(env):
        with open(env, 'w') as arq:
            arquivo = arq.write(' ')

    with open(env, 'r+') as file:
        linhas = file.readlines()
        encontrado = False

        for i, linha in enumerate(linhas):
            if chave in linha:
                linha = linha.rstrip('\n')
                partes_linha = linha.split('"')
                phones_agrupados = partes_linha[1]

                twilio_phones_list = phones_agrupados.split()
                phones_novos = [
                    str(phone)
                    for phone in phones
                    if str(phone) not in twilio_phones_list
                ]

                phones_adicionados = []
                for phone in phones_novos:
                    if phone not in twilio_phones_list:
                        twilio_phones_list.append(phone)
                        phones_adicionados.append(phone)

                if phones_adicionados:
                    phones_agrupados = ' '.join(twilio_phones_list)
                    linha = (
                        f'{partes_linha[0]}"{phones_agrupados}"'
                        f'{partes_linha[2]}\n'
                    )
                    linhas[i] = linha

                for phone in phones_adicionados:
                    print()
                    progress_bar()
                    console.log(f'{chave} {phone} adicionado com sucesso.\n')

                for phone in phones:
                    if str(phone) in twilio_phones_list:
                        if (
                            str(phone) in twilio_phones_list
                            and str(phone) not in phones_adicionados
                        ):
                            print()
                            progress_bar(0.001)
                            console.log(
                                f'O telefone {phone} já existe no arquivo.\n'
                            )

                encontrado = True
                break

        if not encontrado:
            linhas.append(f'{chave}="{" ".join(phones)}"\n')
            print()
            progress_bar()
            console.log(
                f'{chave} {" ".join(phones)} adicionado(s) com sucesso.\n'
            )

        file.seek(0)
        file.writelines(linhas)


@cli.command('show')
def listar(
    destiny_phone: Annotated[
        bool,
        typer.Option(
            help=(
                'Lista todos os números cadastrados '
                'para receber as mensagens;'
            ),
            show_default=False,
        ),
    ] = False,
    sid: Annotated[
        bool,
        typer.Option(
            help='Lista o SID configurado no arquivo de variável;',
            show_default=False,
        ),
    ] = False,
    twilio_phone: Annotated[
        bool,
        typer.Option(
            help=(
                'Lista o TWILIO_PHONE_NUMBER configurado '
                'no arquivo de variável;'
            ),
            show_default=False,
        ),
    ] = False,
    token: Annotated[
        bool,
        typer.Option(
            help=(
                'Lista o TWILIO_AUTH_TOKEN configurado no '
                'arquivo de variável;'
            ),
            show_default=False,
        ),
    ] = False,
):
    """
    Lista todas as variáveis de ambiente cadastradas;
    Usage: palmeiras show --phone;
    Options: --phone, --destiny-phone, --sid, --twilio-phone;

    Args:
        destiny_phone (Annotated[ bool, typer.Option, optional): _description_. Defaults to 'Lista todos os números cadastrados para receber as mensagens;', show_default=False, ), ]=False.
        sid (Annotated[ bool, typer.Option, optional): _description_. Defaults to 'Lista o SID configurado no arquivo de variável;', show_default=False, ), ]=False.
        twilio_phone (Annotated[ bool, typer.Option, optional): _description_. Defaults to 'Lista o TWILIO_PHONE_NUMBER configurado no arquivo de variável;', show_default=False, ), ]=False.
        token (Annotated[ bool, typer.Option, optional): _description_. Defaults to 'Lista o TWILIO_AUTH_TOKEN configurado no arquivo de variável;', show_default=False, ), ]=False.
    """

    option = {
        destiny_phone: 'TWILIO_DESTINY_PHONE_NUMBER',
        sid: 'TWILIO_ACCOUNT_SID',
        twilio_phone: 'TWILIO_PHONE_NUMBER',
        token: 'TWILIO_AUTH_TOKEN',
    }.get(True, None)

    if option is None:
        with open(env, 'r') as fr:
            print()
            console.log(''.join(fr))
        return

    try:
        with open(env, 'r') as fr:
            linhas = fr.readlines()
            valores = [linha for linha in linhas if option in linha]
            if valores:
                print()
                console.log(''.join(valores))
            else:
                print()
                console.log(
                    f'Nenhuma variável de ambiente "{option}" encontrada.\n'
                    f'Para cadastrar tente: '
                    f'\npalmeiras [OPTION] [ARG] ou palmeiras --help\n'
                )
    except IOError:
        print()
        console.log('Erro ao ler o arquivo.\n')


@cli.command()
def delete(
    variavel: Annotated[
        str,
        typer.Argument(
            help='Variável qeu será excluída',
            show_default=False,
        ),
    ]
):
    """
    Exclui uma das configurações do arquivo de variável de ambiente.

    Ex: palmeiras delete sid
    """
    option = {
        'destiny_phone': 'TWILIO_DESTINY_PHONE_NUMBER',
        'sid': 'TWILIO_ACCOUNT_SID',
        'twilio_phone': 'TWILIO_PHONE_NUMBER',
        'token': 'TWILIO_AUTH_TOKEN',
    }
    with open(env, 'r') as file:
        variaveis = file.readlines()

        for i, item in enumerate(variaveis):
            if option[variavel] in variaveis[i]:
                variaveis.remove(item)
                print()
                progress_bar()
                console.log(f'{option[variavel]} removido com sucesso.\n')
                with open(env, 'w') as fw:
                    arquivo = fw.write(''.join(variaveis))
                return
        else:
            print()
            progress_bar(0.001)
            console.log(f'O arquivo não contém nenhum {option[variavel]}.\n')


# if __name__ == '__main__':
#     cli()
