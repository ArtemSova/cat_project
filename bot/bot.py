from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.core.handlers import user_commands_router
from bot.core.middlewares import DataBaseSession
from config import BOT_TOKEN, ADMINS_LIST
from app.database import session_factory


bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
bot.my_admins_list = list(map(int, ADMINS_LIST.split()))

dp = Dispatcher()

user_commands_router.message.middleware(DataBaseSession(session_pool=session_factory))

dp.include_router(user_commands_router)  # Подключаем роутер только тут

