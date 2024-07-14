import asyncio
import logging

import telegram
from rocketry import Grouper
from rocketry.args import Return
from rocketry.conds import after_finish

from app.config.settings import BotSettings
from app.tasks.formata import formata_texto

group = Grouper(execution='async')
settings = BotSettings()


@group.task(after_finish(formata_texto))
async def enviar_msg(texto: str = Return(formata_texto)) -> None:
    """
    Envia a mensagem para os números configurados no arquivo de variável de ambiente.

    Args: Argumentos:
        texto (str): Texto ja formatado e pronto para envio. Texto de retorno da função formata_texto().
    """
    try:
        bot = telegram.Bot(settings.BOT_TOKEN)
        async with bot:
            await bot.send_message(text=texto, chat_id=settings.BOT_ID)

    except telegram.error.TelegramError as erro:    # pragma: no cover
        logging.error(f'Não foi possível enviar a mensagem: {erro}')
