import random
import re

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, user
from config import bot
from aiogram import types, Dispatcher

from database.sql_commands import Database
from keybords.start_kb import quiz_1_keyboard, quiz_2_keyboard, like_dislike_keyboard


async def quiz_1(message: types.Message):
    question = "Who invented Python"
    options = [
        "Voldemort",
        "Harry Potter",
        "Linus Torvalds",
        "Guido Van Rossum",
        "Witch"
    ]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=options,
        is_anonymous=False,
        type='quiz',
        correct_option_id=3,
        reply_markup=await quiz_1_keyboard()
    )


async def quiz_2(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Male or Female ?",
        reply_markup=await quiz_2_keyboard()
    )


async def answer_male(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="You are male"
    )


async def answer_female(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text='You are female'
    )


async def admin_user_call(call: types.CallbackQuery):
    users = Database().sql_admin_select_user_command()

    if users is None:
        await call.message.reply("No users found.")
        return

    print(users)
    data = []
    for user in users:
        if not user["username"]:
            data.append(f"[{user['first_name']}](tg://user?id={user['telegram_id']})")
        else:
            data.append(f"[{user['first_name']}](tg://user?id={user['telegram_id']})")

    data = '\n'.join(data)
    await call.message.reply(text=data, parse_mode=types.ParseMode.MARKDOWN)


async def my_profile_call(call: types.CallbackQuery):
    user_form = Database().sql_select_user_form_by_telegram_id_command(telegram_id=call.from_user.id)

    if user_form:
        user_data = user_form[0]

        with open(user_data['photo'], 'rb') as photo:
            await bot.send_photo(
                chat_id=call.from_user.id,
                photo=photo,
                caption=f"*Nickname:* {user_data['nickname']}\n"
                        f"*Age:* {user_data['age']}\n"
                        f"*Bio* {user_data['bio']}\n"
                        f"*Married* {user_data['married']}\n",
                parse_mode=types.ParseMode.MARKDOWN
            )
    else:
        await bot.send_message(chat_id=call.from_user.id, text="Профиль не найден.")


async def random_profiles_call(call: types.CallbackQuery):
    user_forms = Database().sql_select_user_forms_command()
    print(user_forms)
    random_form = random.choice(user_forms)
    print(random_form)
    with open(random_form['photo'], 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=f"*Nickname:* {random_form['nickname']}\n"
                    f"*Age:* {random_form['age']}\n"
                    f"*Bio* {random_form['bio']}\n"
                    f"*Married* {random_form['married']}\n",
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=await like_dislike_keyboard(
                telegram_id=random_form["telegram_id"]
            )
        )


async def like_call(call: types.CallbackQuery):
    owner_telegram_id = re.sub("like_button_", "", call.data)
    print(owner_telegram_id)
    is_like_existed = Database().sql_insert_like_form_command(
        owner_telegram_id=owner_telegram_id,
        liker_telegram_id=call.from_user.id
    )
    if is_like_existed:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Ты уже лайкал эту анкету"
        )
    else:
        Database().sql_select_liked_form_command(
            owner_telegram_id=owner_telegram_id,
            liker_telegram_id=call.from_user.id
        )
        await bot.send_message(
            chat_id=owner_telegram_id,
            text="Кто-то вас лайкнул"
        )


def register_callback_handlers(dp: Dispatcher):
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_call_1")
    dp.register_callback_query_handler(answer_male, lambda call: call.data == "answer_male")
    dp.register_callback_query_handler(answer_female, lambda call: call.data == "answer_female")
    dp.register_callback_query_handler(admin_user_call, lambda call: call.data == "admin_user_list")
    dp.register_callback_query_handler(my_profile_call, lambda call: call.data == "my_profile")
    dp.register_callback_query_handler(random_profiles_call, lambda call: call.data == "random_profiles")
    dp.register_callback_query_handler(like_call, lambda call: "like_button_" in call.data)
