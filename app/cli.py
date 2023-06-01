import typer

app = typer.Typer()


def adicionar_linha(chave: str, valor: str):
    with open('teste.txt', 'r+') as arquivo:
        linhas = arquivo.readlines()
        if not any(chave in linha for linha in linhas):
            arquivo.write(f'\n{chave}="{valor}"')
            typer.echo(f'{chave} adicionada com sucesso!')
        else:
            typer.echo(f'{chave} já existente no arquivo.')


@app.command()
def sid(sid: str):
    """
    Adiciona o SID da conta Twilio na variável de ambiente.

    Examplo: palmeiras sid klashkamqpíshkdji987

    """
    adicionar_linha('TWILIO_SID', sid)


@app.command()
def token(token: str):
    """
    Adiciona o TOKEN da conta Twilio na variável de ambiente.

    Exemplo: ```palmeiras token ksjhkjashkfahkjsfhalsfhlajshfklajsfka```

    """
    adicionar_linha('TWILIO_TOKEN', token)


@app.command()
def phone(phone: str):
    """
    Adiciona o seu PHONE_NUMBER da conta Twilio na variável de ambiente.

    Exemplo: ```palmeiras phone ksjhkjashkfahkjsfhalsfhlajshfklajsfka```

    """
    adicionar_linha('TWILIO_PHONE_NUMBER', phone)


@app.command()
def destiny_phone(phone: str):
    """
    Adiciona números de destino para onde serão enviadas as mensagens.

    Exemplo: ```palmeiras destiny_phone +5511973675725```

    """
    chave = 'DESTINY_PHONE_NUMBER'
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
            print(''.join(numeros_telefone).strip())
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


@app.command()
def listar(
    destiny_phone: bool = False,
    sid: bool = False,
    twilio_phone: bool = False,
    token: bool = False,
):
    """
    Lista todas as variáveis de ambiente cadastradas.
    Args: --phone, --destiny-phone, --sid, --twilio-phone
    Exemplo: ```palmeiras listar --sid```

    """

    option = {
        destiny_phone: 'DESTINY_PHONE_NUMBER',
        sid: 'TWILIO_SID',
        twilio_phone: 'TWILIO_PHONE_NUMBER',
        token: 'TWILIO_TOKEN',
    }.get(True, None)

    if option is None:
        typer.echo(
            'Nenhuma opção selecionada. Por favor,'
            'escolha uma das opções --phone ou --sid.'
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
                    f"Nenhuma variável de ambiente '{option}' encontrada."
                )
    except IOError:
        typer.echo('Erro ao ler o arquivo.')


if __name__ == '__main__':
    app()
