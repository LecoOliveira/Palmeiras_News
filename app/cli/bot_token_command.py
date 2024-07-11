import asyncio

import telegram
import typer
from typing_extensions import Annotated

from app.cli.config_cli import adicionar_credencial
from app.config.settings import Settings

cli = typer.Typer()
settings = Settings()


async def get_id(token: str, env: str) -> None:    # pragma: no cover
    """
    Pega o ID do usuário que enviou mensagem para o bot, e armazena no .env.

    Args Argumentos:
        token (str): Token recebido na função bot_token.
        env (str): Arquivo que será armazenada a variável de ambiente.
    """
    bot = telegram.Bot(token)
    async with bot:
        id_ = (await bot.get_updates())[0].message.from_user.id
        adicionar_linha('BOT_ID', id_, env)


@cli.callback(
    invoke_without_command=True,
    help='Configura o BOT_TOKEN na variável de ambiente.',
)
def bot_token(
    token: Annotated[
        str,
        typer.Argument(
            help='Seu TOKEN gerado ao criar o bot',
            show_default=False,
        ),
    ],
    env: Annotated[
        str,
        typer.Option(
            help='Arquivo que será armazenada a variável de ambiente'
        ),
    ] = settings.ENV,
) -> None:
    """
    Adiciona o TOKEN da do seu bot na variável de ambiente;

    Comando: `palmeiras bot_token YOUR_BOT_TOKEN`

    Args: Argumentos:
        sid (str): Seu TOKEN gerado ao criar o bot no Bot_Father.
        env (str): Arquivo que será armazenada a variável de ambiente.
    """
    adicionar_credencial('BOT_TOKEN', token, env)
    asyncio.run(get_id(token, env))
