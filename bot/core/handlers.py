from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.formatting import as_list, as_marked_section, Bold

from sqlalchemy.ext.asyncio import AsyncSession

from app.database import session_factory
from app.models import Cats
from app.orm import orm_add_user, orm_add_new_cat, orm_change_password, orm_show_all_cats
from bot.core.filters import ChatTypeFilter
from bot.core.keyboard import start_kb


user_commands_router = Router()
user_commands_router.message.filter(ChatTypeFilter(['private']))


# реакция на '/start'
@user_commands_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    try:
        await orm_add_user(
            session,
            user_tg_id=message.from_user.id,
            user_name=message.from_user.username,
            password="GqjH5B0mhT63VcGsIp1",
            phone_number=None,
        )
        await message.answer('Котики приветствуют тебя!', reply_markup=start_kb)
    except:
        await message.answer('Котики приветствуют тебя!', reply_markup=start_kb)

#--------------------------------------Показать список всех котиков------------------------------------------
@user_commands_router.message(F.text == "Все котики")
async def cats_cmd(message: types.Message, session: AsyncSession):
    result = await orm_show_all_cats(session)

    if not result:
        await message.answer("Нет ни одного котика")
        return

    response = "Это все котики: \n"
    for cat in result:
        response += f"Имя котика: {cat.cat_name}, цвет: {cat.cat_color}, возраст: {cat.cat_age} \n"

    await message.answer(response)

# ---------------------------------Добавление нового котика--------------------------------------------------
# FSM состояния для внесения нового котика
class NewCat(StatesGroup):
    cat_name = State()
    cat_color = State()
    cat_age = State()

@user_commands_router.message(StateFilter(None), F.text == "Новый котик")
async def new_cat_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите имя нового котика или введите "отмена", чтобы вернуться в меню',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(NewCat.cat_name)                    # Ждем получения (ввода) имени


@user_commands_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def break_cmd(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Все действия отменены", reply_markup=start_kb)


@user_commands_router.message(NewCat.cat_name, F.text)
async def new_cat_name_cmd(message: types.Message, state: FSMContext):
    await state.update_data(cat_name=message.text)
    await message.answer(
        'Введите цвет котика или введите "отмена", чтобы вернуться в меню',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(NewCat.cat_color)                    # Ждем получения (ввода) цвета

# Пользователь отправил некорректные данные
@user_commands_router.message(NewCat.cat_name)
async def new_cat_name_cmd(message: types.Message, state: FSMContext):
    await message.answer('Вы ввели некорректное имя. Введите имя котика или введите "отмена", чтобы вернуться в меню')


@user_commands_router.message(NewCat.cat_color, F.text)
async def new_cat_color_cmd(message: types.Message, state: FSMContext):
    await state.update_data(cat_color=message.text)
    await message.answer(
        'Введите возраст котика или введите "отмена", чтобы вернуться в меню',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(NewCat.cat_age)

@user_commands_router.message(NewCat.cat_color)
async def new_cat_color_cmd(message: types.Message, state: FSMContext):
    await message.answer('Вы ввели некорректный цвет. Введите цвет котика или введите "отмена", чтобы вернуться в меню')


@user_commands_router.message(NewCat.cat_age, F.text)
async def new_cat_age_cmd(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(cat_age=int(message.text))
    await message.answer("Новый котик добавлен", reply_markup=start_kb)
    data = await state.get_data()
    # Запись в бд через функцию из orm
    await orm_add_new_cat(session, data)
    # Очистка состояний из памяти
    await state.clear()

@user_commands_router.message(NewCat.cat_age)
async def new_cat_color_cmd(message: types.Message, state: FSMContext):
    await message.answer('Вы ввели некорректный возраст. Введите возраст котика или введите "отмена", чтобы вернуться в меню')

# --------------------------Работа с регистрацией на сайте---------------------------------------------------
class NewAcc(StatesGroup):
    password = State()

@user_commands_router.message(F.text == "Создать/изменить пароль для сайта")
async def login_cmd(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите новый пароль или введите "отмена", чтобы вернуться в меню',
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.set_state(NewAcc.password)

@user_commands_router.message(NewAcc.password, F.text)
async def new_cat_age_cmd(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(password=message.text)
    await message.answer("Пароль обновлен", reply_markup=start_kb)
    data = await state.get_data()
    await orm_change_password(session, message.from_user.id, password=data["password"])

    await state.clear()

@user_commands_router.message(NewAcc.password)
async def new_cat_color_cmd(message: types.Message, state: FSMContext):
    await message.answer('Вы ввели некорректный пароль. Введите пароль или введите "отмена", чтобы вернуться в меню')






