from telethon import TelegramClient, events
import os
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from telethon.events.newmessage import NewMessage
from telethon.tl.patched import Message
from dataclasses import dataclass

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.FileHandler('Notes/debug.log')]
)

# Telethon setup
api_id = int(os.getenv('TG_APP_API_ID'))
api_hash = os.getenv('TG_APP_API_HASH')
client = TelegramClient('sessions/client', api_id=api_id, api_hash=api_hash)

# Telebot setup
bot_token = os.getenv('FreelancehuntNotifier_bot_TOKEN')
bot = TeleBot(token=bot_token)

# User setup
chat_id = 392896704
channel_to_listen = 'https://t.me/FreelancehuntProjects'
tag = '#парсинг_данных'


@dataclass
class ParsedMessage:
    text: str
    button_text: str
    button_url: str


@client.on(events.NewMessage(chats=channel_to_listen, pattern=rf'(.|\n)*{tag}'))
async def listen_to_new_message(event: NewMessage.Event) -> None:
    parsed_message = await parse_message(event)
    await send_notification(parsed_message)


async def parse_message(event: NewMessage.Event) -> ParsedMessage:
    message: Message = event.message
    button = message.reply_markup.rows[0].buttons[0]
    parsed_message = ParsedMessage(
        text=message.message,
        button_text=button.text,
        button_url=button.url
    )
    return parsed_message


async def send_notification(parsed_message: ParsedMessage) -> None:
    bot.send_message(chat_id=chat_id,
                     text=parsed_message.text,
                     reply_markup=InlineKeyboardMarkup([
                         [InlineKeyboardButton(text=parsed_message.button_text,
                                               url=parsed_message.button_url)]])
                     )


with client:
    try:
        client.run_until_disconnected()
    except Exception as ex:
        print(ex)
