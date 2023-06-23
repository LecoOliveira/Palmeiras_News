import os
import subprocess
import time
from re import compile
from typing import List

import typer
from rich.console import Console
from rich.progress import track
from typing_extensions import Annotated

cli = typer.Typer(
    help='Interface para configuração de variáveis '
    'de ambiente que serão usadas no Palmeiras_news.'
)
console = Console()
env = '.env'


def progress_bar(time_: float = 0.02, description: str = 'Configurando...'):
    print()
    total = 0
    for value in track(range(100), description=description):
        time.sleep(time_)
        total += 1


def adicionar_linha(chave: str, valor: List[str], env: str = env):
    """
    Função principal que adiciona os dados no arquivo de variável de ambiente.

    Args:
        chave (str): Recebe a chave da variável a ser criada.
        valor (List[str]): Recebe o valor da chave criada.
        env (str): Recebe o arquivo que será configurada a variável de ambiente.
    Exemplo:
        O resultado final ficará assim:
        ```CHAVE_DA_VARIAVEL="valor_da_variavel"```
    """
    if chave != 'TWILIO_DESTINY_PHONE_NUMBER':
        if not os.path.exists(env):
            open(env, 'w').close()

        with open(env, 'r+') as arquivo:
            linhas = arquivo.readlines()
            if not any(chave in linha for linha in linhas):
                arquivo.write(f'{chave}="{valor}"\n')
                progress_bar()
                console.log(f'{chave} configurado com sucesso!\n')
            else:
                progress_bar(0)
                console.log(
                    f'{chave} [b][red]já existe[/red][/b] no arquivo.\n'
                )
    else:
        if not os.path.exists(env):
            open(env, 'w').close()

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
                        phone
                        for phone in valor
                        if phone not in twilio_phones_list
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
                        progress_bar()
                        console.log(
                            f'{chave} {phone} configurado com sucesso.\n'
                        )

                    for phone in valor:
                        if (
                            phone in twilio_phones_list
                            and phone not in phones_adicionados
                        ):
                            progress_bar(0.001)
                            console.log(
                                f'O telefone {phone} já existe no arquivo.\n'
                            )

                    encontrado = True
                    break

            if not encontrado:
                linhas.append(f'{chave}="{" ".join(valor)}"\n')
                progress_bar()
                console.log(
                    f'{chave} {" ".join(valor)} configurado(s) com sucesso.\n'
                )

            file.seek(0)
            file.writelines(linhas)


@cli.command(help='Configura o TWILIO_ACCOUNT_SID na variável de ambiente.')
def sid(
    sid: Annotated[
        str,
        typer.Argument(
            help='Seu SID gerado ao efetuar cadastro na Twilio',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(
            help='Arquivo que será armazenada a variável de ambiente'
        ),
    ] = env,
):
    """
    Adiciona o SID da conta Twilio na variável de ambiente;

    Comando: `palmeiras sid YOUR_TWILIO_ACCOUNT_SID`

    Args: Argumentos:
        sid (str): Seu SID gerado ao efetuar cadastro na Twilio.
        env (str): Arquivo que será armazenada a variável de ambiente.
    """
    adicionar_linha('TWILIO_ACCOUNT_SID', sid, env)


@cli.command(help='Configura o TWILI_AUTH_TOKEN na variável de ambiente.')
def token(
    token: Annotated[
        str,
        typer.Argument(
            help='Token gerado ao efetuar cadastro na Twilio',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(
            help='Arquivo onde será armazenada a variável de ambiente.'
        ),
    ] = env,
):
    """
    Adiciona o TOKEN da conta Twilio na variável de ambiente;

    Comando: `palmeiras token YOUR_TWILIO_AUTH_TOKEN`

    Args: Argumentos:
        token (str): Token gerado ao efetuar cadastro na Twilio.
        env (str): Arquivo onde será armazenada a variável de ambiente.
    """
    adicionar_linha('TWILIO_AUTH_TOKEN', token, env)


@cli.command(help='Configura o TWILIO_PHONE_NUMBER na variável de ambiente.')
def twilio_phone(
    phone: Annotated[
        str,
        typer.Argument(
            help='Número americano gerado pela Twilio',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(
            help='Arquivo onde será configurado o TWILIO_PHONE_NUMBER.'
        ),
    ] = env,
):
    """
    Adiciona o seu PHONE_NUMBER da conta Twilio na variável de ambiente;

    Comando: `palmeiras twilio-phone YOUR_TWILIO_PHONE`

    Args: Argumentos:
        phone (str): Número americano gerado pela Twilio.
        env (str): Arquivo onde será configurado o TWILIO_PHONE_NUMBER.
    """
    adicionar_linha('TWILIO_PHONE_NUMBER', phone, env)


@cli.command(
    help='Configura os números para onde serão enviadas as mensagens.'
)
def destiny_phone(
    phones: Annotated[
        List[str],
        typer.Argument(
            help='Um ou mais destiny_phone que deseja configurar '
            '(números devem ser separados por espaço); '
            'Ex: +551199999999 +5511999999999',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(
            help='Arquivo que será armazenada a variável de ambiente'
        ),
    ] = env,
):
    """
    Adiciona números de destino para onde serão enviadas as mensagens;

    Comando: `palmeiras destiny-phone YOUR_TWILIO_DESTINY_PHONES`

    Args: Argumentos:
        phones (List[str]): Um ou mais telefones que deseja configurar para que possam receber as mensagens (números devem ser separados por espaço) Ex: +551199999999 +5511999999999.
        env (str): Arquivo que será armazenada a variável de ambiente.
    """
    padrao = compile(r'^\+\d{2,3}\d{2}\d{4,5}\d{4}$')

    numeros_validos = [
        phone for i, phone in enumerate(phones) if padrao.match(phones[i])
    ]
    numeros_invalidos = [
        phone for i, phone in enumerate(phones) if not padrao.match(phones[i])
    ]

    if numeros_invalidos:
        console.log(
            f'\nNúmero(s) {" ".join(numeros_invalidos)} inválido(s). '
            'O número deve conter o formato +xxxxxxxxxxxxx '
            '(Começando com o sinal "+" e ter entre 12 e 14 números).\n'
        )
        return

    adicionar_linha('TWILIO_DESTINY_PHONE_NUMBER', numeros_validos, env)


@cli.command(help=('Lista todas as variáveis de ambiente cadastradas'))
def listar(
    destiny_phone: Annotated[
        bool,
        typer.Option(
            help=(
                'Lista todos os TWILIO_DESTINY_PHONE_NUMBER cadastrados '
                'para receber as mensagens;'
            ),
            show_default=False,
        ),
    ] = False,
    sid: Annotated[
        bool,
        typer.Option(
            help='Lista o TWILIO_ACCOUNT_SID configurado no arquivo de variável;',
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
    env: Annotated[
        str,
        typer.Option(help='Arquivo de onde será lido a variável de ambiente'),
    ] = env,
):
    """
    Lista todas as variáveis de ambiente cadastradas.

    Exemplos:
        Para listar todas as variáveis:
        ```bash
        $ palmeiras listar

        [15:13:50] TWILIO_ACCOUNT_SID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                   TWILIO_AUTH_TOKEN="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                   TWILIO_DESTINY_PHONE_NUMBER="+xxxxxxxxxxxxx"
                   TWILIO_PHONE_NUMBER="+xxxxxxxxxxxxx"
        ```
        Para listar uma variável específica:
        ```bash
        $ palmeiras listar --sid

        [11:41:16] TWILIO_ACCOUNT_SID="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        ```

    Opções: `--token, --destiny-phone, --sid, --twilio-phone`

    Args: Argumentos:
        destiny_phone (bool): Lista todos os números cadastrados para receber as mensagens.
        sid (bool): Lista o SID configurado no arquivo de variável.
        twilio_phone (bool): Lista o TWILIO_PHONE_NUMBER configurado no arquivo de variável.
        token (bool): Lista o TWILIO_AUTH_TOKEN configurado no arquivo de variável.
        env (str): Arquivo de onde buscar as variáveis.
    """

    option = {
        destiny_phone: 'TWILIO_DESTINY_PHONE_NUMBER',
        sid: 'TWILIO_ACCOUNT_SID',
        twilio_phone: 'TWILIO_PHONE_NUMBER',
        token: 'TWILIO_AUTH_TOKEN',
    }.get(True, None)

    if option is None:
        try:
            with open(env, 'r') as arquivo:
                console.log(f'\n{"".join(arquivo)}')
            return
        except FileNotFoundError:
            console.log(
                f'\nNenhum arquivo {env} encontrado.\n'
                'Tente sem o "--env", ou rode "palmeiras listar '
                '--help" para obter ajuda.\n'
            )
            return

    try:
        with open(env, 'r') as arquivo:
            linhas = arquivo.readlines()
            valores = [linha for linha in linhas if option in linha]
            if valores:
                console.log(f'\n{"".join(valores)}\n')
            else:
                console.log(
                    f'\nNenhuma variável de ambiente "{option}" encontrada.\n'
                    f'Para cadastrar tente:'
                    f'\npalmeiras [OPTION] [ARG] ou palmeiras --help\n'
                )
    except IOError:
        console.log(
            '\nErro ao ler o arquivo. Você deve configurar alguma '
            'variável antes de tentar listá-las\n'
        )


@cli.command(help='Comando que deleta uma variável de ambiente do arquivo.')
def delete(
    variavel: Annotated[
        str,
        typer.Argument(
            help='Variável que será excluída',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(help='Arquivo de onde a função vai deletar a variável'),
    ] = env,
):
    """
    Comando do CLI que deleta uma variável de ambiente do arquivo.

    Comando: `palmeiras delete VARIÁVEL_QUE_DESEJA_EXCLUIR`

    Args: Argumentos:
        variavel (str): Variável que será excluída.
        env (str): Arquivo de onde a função vai deletar a variável.
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
                progress_bar(description='Removendo...')
                console.log(f'{option[variavel]} removido com sucesso.\n')
                with open(env, 'w') as fw:
                    arquivo = fw.write(''.join(variaveis))
                return
        else:
            progress_bar(0.001, description='Removendo...')
            console.log(f'O arquivo não contém nenhum {option[variavel]}.\n')
