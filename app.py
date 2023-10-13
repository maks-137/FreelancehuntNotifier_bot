from telethon import TelegramClient, events
import os
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from telethon.events.newmessage import NewMessage
from telethon.tl.patched import Message

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.FileHandler('Notes/debug.log'),
              logging.StreamHandler()
              ]
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


@client.on(events.NewMessage(chats=channel_to_listen))
async def listen_to_new_message(event: NewMessage.Event) -> None:
    message: Message = event.message
    if is_message_valid(message):
        send_notification(message)


def is_message_valid(message: Message):
    if tag in message.message:
        return True
    else:
        return False


def send_notification(message: Message) -> None:
    button = message.reply_markup.rows[0].buttons[0]
    bot.send_message(chat_id=chat_id,
                     text=message.message,
                     reply_markup=InlineKeyboardMarkup([
                         [InlineKeyboardButton(text=button.text,
                                               url=button.url)]
                     ]))


with client:
    try:
        client.run_until_disconnected()
    except Exception as ex:
        print(ex)
