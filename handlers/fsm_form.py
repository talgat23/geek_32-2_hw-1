from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from config import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.sql_commands import Database
from keybords.fsm_keyboard import select_my_profile_keyboard


class FormStates(StatesGroup):
    nickname = State()
    age = State()
    bio = State()
    married = State()
    photo = State()


async def fsm_start(messages: types.Message):
    await messages.reply("Отправь мне свой никнейм")
    await FormStates.nickname.set()


async def load_nickname(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text

    await FormStates.next()
    await message.reply("Отправь мне свой возраст, используй только числа")


async def load_age(message: types.Message,
                   state: FSMContext):
    try:
        if type(int(message.text)) != int:
            await message.reply("Только числа!!!"
                                " Пожалуйста запустите регистрация заново")
            await state.finish()
        else:
            async with state.proxy() as data:
                data['age'] = message.text
            await FormStates.next()
            await message.reply("Отправь мне свою биография или хобби")
    except ValueError as e:
        await state.finish()
        print(f"FSMAGE: {e}")
        await message.reply("Только числа!!!"
                            "Пожалуйста запустите регистрация заново")


async def load_bio(message: types.Message,
                   state: FSMContext):
    async with state.proxy() as data:
        data['bio'] = message.text
    await FormStates.next()
    await message.reply("Вы женаты/замужем? "
                        "(если не хотите отвечать, отправьте знак минус)")


async def load_married(message: types.Message,
                       state: FSMContext):
    async with state.proxy() as data:
        data['married'] = message.text
    await FormStates.next()
    await message.reply("Отправь мне свое фото (не в разрешении файла)")


async def load_photo(message: types.Message,
                     state: FSMContext):
    print(message.photo)
    path = await message.photo[-1].download(
        destination_dir="/Users/talgatchekirov/PycharmProjects/geek_32-2/media"
    )
    async with state.proxy() as data:
        Database().sql_insert_user_form_command(
            telegram_id=message.from_user.id,
            nickname=data['nickname'],
            age=data['age'],
            bio=data['bio'],
            married=data['married'],
            photo=path.name,
        )
        await message.reply("Вы успешно зарегистрировали свою анкету.\n"
                            "Можете посмотреть анкету, нажав на кнопку 'Мой профиль'.",
                            reply_markup=await select_my_profile_keyboard())


def register_fsm_form_handlers(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=["signup"])
    dp.register_message_handler(load_nickname,
                                state=FormStates.nickname,
                                content_types=['text'])
    dp.register_message_handler(load_age,
                                state=FormStates.age,
                                content_types=['text'])
    dp.register_message_handler(load_bio, state=FormStates.bio,
                                content_types=['text'])
    dp.register_message_handler(load_married,
                                state=FormStates.married,
                                content_types=['text'])
    dp.register_message_handler(load_photo,
                                state=FormStates.photo,
                                content_types=ContentTypes.PHOTO)
