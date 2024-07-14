from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import telegram
from telegram.error import TelegramError

from app.config.settings import BotSettings
from app.tasks.envia import enviar_msg, settings
from app.tasks.formata import formata_texto
from app.tasks.texto import sem_dados, texto_msg

test_link = 'https://www.palmeiras.com.br/jogo/?idjogo=2588'
test_hora_jogo = datetime.now().strftime('%H:%M')

result = texto_msg(test_link)


# texto_msg tests --------------------------------------------------


def test_texto_msg_nao_deve_retornar_None():
    assert result is not None


def test_texto_msg_deve_retornar_algum_texto_em_uma_lista():
    assert isinstance(result, list)


def test_texto_msg_nao_esta_vazio():
    assert len(result) > 0


# formata_texto tests ----------------------------------------------


def test_formata_texto_deve_retronar_um_str():
    assert isinstance(formata_texto(texto=result), str)


def test_formata_texto_deve_retornar_aviso_caso_nao_tenha_dados_do_jogo():
    assert formata_texto(texto=list({sem_dados})) == sem_dados


# enviar_msg tests ----------------------------------------------


@pytest.mark.asyncio
async def test_enviar_msg():
    texto_formatado = 'Texto de teste formatado'
    mock_bot = MagicMock()
    mock_bot.send_message = AsyncMock()

    telegram.Bot = lambda token: mock_bot

    result = await enviar_msg(texto_formatado)

    mock_bot.send_message.assert_called_once_with(
        text=texto_formatado, chat_id=settings.BOT_ID
    )
