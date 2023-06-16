from os import getenv

from dotenv import load_dotenv

load_dotenv()

phones = getenv('TWILIO_DESTINY_PHONE_NUMBER').split(' ')
ACCOUNT_SID = getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = getenv('TWILIO_PHONE_NUMBER')
