import sqlite3
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot
from aiogram import types, Dispatcher

from const import START_MENU_TEXT
from database import sql_commands
from keybords.start_kb import admin_select_users_keyboard, start_keyboard, new_start_keyboard


def random_profiles_button():
    pass


async def start_button(message: types.Message):
    sql_commands.Database().sql_insert_user_command(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    print(message)
    with open("/Users/talgatchekirov/PycharmProjects/geek_32-2/media/animation.gif", 'rb') as animation:
        await bot.send_animation(
            chat_id=message.chat.id,
            animation=animation,
            caption=START_MENU_TEXT.format(
                user=message.from_user.username
            ),
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=await new_start_keyboard()
        )


async def secret_word(message: types.Message):
    if message.from_user.id == 439193198:
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=message.message_id
        )
        await bot.send_message(
            chat_id=message.from_user.id,
            text="Yes sir",
            reply_markup=await admin_select_users_keyboard()
        )


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
    dp.register_message_handler(secret_word, lambda word: 'dorei' in word.text)
