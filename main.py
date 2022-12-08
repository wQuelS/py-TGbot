import os
from dotenv import load_dotenv
import telebot

load_dotenv()

TOKEN = os.environ.get("API_KEY")
tg_bot = telebot.TeleBot(TOKEN)
URL = "https://paper-trader.frwd.one"
VALID_PAIRS = ("BTCUSDT", "BNBUSDT", "ETHUSDT",)
TIMEFRAME = ("5m", "15m", "1h", "4h", "1d", "1w", "1M",)


def validate_pairs(message):
    pair = message.text
    if pair in VALID_PAIRS:
        return True
    return False


@tg_bot.message_handler(commands=["start"])
def start_message(message):
    tg_bot.send_message(
        message.chat.id,
        f"Hello, please pick one crypto-pair among available pairs: {VALID_PAIRS}",
    )


tg_bot.polling()
