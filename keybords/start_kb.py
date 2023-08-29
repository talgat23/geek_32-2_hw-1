from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)


async def start_keyboard():
    quiz_button = KeyboardButton("/quiz")
    mark_up = ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True
    )
    mark_up.add(quiz_button)
    return mark_up


async def quiz_1_keyboard():
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "Следующая Викторина",
        callback_data="button_call_1"
    )
    markup.add(button_call_1)
    return markup


async def quiz_2_keyboard():
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "Male",
        callback_data="answer_male"
    )
    button_call_2 = InlineKeyboardButton(
        "Female",
        callback_data="answer_female"
    )
    markup.row(
        button_call_1,
        button_call_2
    )
    return markup


async def admin_select_users_keyboard():
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "список пользователей",
        callback_data="admin_user_list"
    )
    markup.row(
        button_call_1,
    )
    return markup


async def new_start_keyboard():
    markup = InlineKeyboardMarkup()
    random_profiles_button = InlineKeyboardButton(
        "Просмотр анкет",
        callback_data="random_profiles"
    )
    markup.row(
        random_profiles_button,
    )
    return markup


async def like_dislike_keyboard(telegram_id):
    markup = InlineKeyboardMarkup(row_width=2)
    like_button = InlineKeyboardButton(
        ":like:",
        callback_data=f"like_button_{telegram_id}"
    )
    dislike_button = InlineKeyboardButton(
        ":Dislike:",
        callback_data=f"random_profiles"
    )
    markup.row(
        like_button,
        dislike_button
    )
    return markup
