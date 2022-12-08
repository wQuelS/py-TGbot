import os

import requests
from dotenv import load_dotenv
import telebot
import random
from bs4 import BeautifulSoup


load_dotenv()

TOKEN = os.environ.get("API_KEY")
tg_bot = telebot.TeleBot(TOKEN)
URL = "https://paper-trader.frwd.one"
VALID_PAIRS = (
    "BTCUSDT",
    "BNBUSDT",
    "ETHUSDT",
)
TIMEFRAME = (
    "5m",
    "15m",
    "1h",
    "4h",
    "1d",
    "1w",
    "1M",
)


def validate_pairs(message):
    pair = message.text
    if pair in VALID_PAIRS:
        return True
    return False


def get_image(message):
    random_data = {
        "pair": message.text,
        "timeframe": random.choice(TIMEFRAME),
        "candles": random.randint(1, 1000),
        "ma": random.randint(1, 50),
        "tp": random.randint(1, 100),
        "sl": random.randint(1, 100),
    }

    response = requests.post(URL, data=random_data)
    soup = BeautifulSoup(response.text, "html.parser")
    image_source = soup.find("img")["src"]
    return image_source[1:]


@tg_bot.message_handler(commands=["start", "again"])
def start_message(message):
    tg_bot.send_message(
        message.chat.id,
        f"Hello, please pick one crypto-pair among available pairs: {VALID_PAIRS}",
        parse_mode="html",
    )


@tg_bot.message_handler()
def send_image(message):
    if validate_pairs(message):
        tg_bot.send_photo(
            message.chat.id,
            f"{URL}{get_image(message)}",
            "If you want to pick another pair click here -> /again",
        )
    else:
        tg_bot.send_message(
            message.chat.id,
            "Please choose correct crypto pair. To see available pairs input /start",
            parse_mode="html",
        )


tg_bot.polling()
