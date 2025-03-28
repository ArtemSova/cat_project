import asyncio
import uvicorn
from fastapi import FastAPI

from app.router import router
from app.orm import init_db
from app.database import session_factory
from bot.bot import bot, dp  # Импортируем готовый бот и диспетчер
from bot.core.middlewares import DataBaseSession

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup():
    await init_db()
    asyncio.create_task(run_bot())  # Запускаем бота в фоне

def run_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

async def bot_startup(bot):
    print('======================== БОТ ВКЛЮЧЕН =============================')

async def bot_shutdown(bot):
    print('======================== БОТ ОТКЛЮЧЕН ============================')

async def run_bot():
    dp.startup.register(bot_startup)
    dp.shutdown.register(bot_shutdown)

    # dp.update.middleware(DataBaseSession(session_pool=session_factory))

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await bot.set_my_name('Бот Котиков')
    except:
        pass

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    run_fastapi()











