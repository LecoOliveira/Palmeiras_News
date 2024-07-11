from dataclasses import dataclass
from os import getenv
from pathlib import Path
from typing import Dict

from dotenv import load_dotenv
from pydantic import BaseSettings

path = Path.cwd()
load_dotenv('.env')
load_dotenv(f'{path}/app/config/config.env')


class BotSettings(BaseSettings):
    BOT_TOKEN: str
    BOT_ID: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Settings(BaseSettings):
    URL_PRINCIPAL: str
    HEADERS: Dict[str, str]
    ENV: str

    class Config:
        env_file = 'config.env'
        env_file_encoding = 'utf-8'
