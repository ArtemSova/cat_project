import asyncio
import uvicorn
from redis import asyncio as aioredis
from fastapi import FastAPI

from app.router import router
from app.orm import init_db
from config import REDIS_URL
from bot.bot import bot, dp  # Импортируем готовый бот и диспетчер


app = FastAPI()
app.include_router(router)

redis = aioredis.from_url(REDIS_URL)

@app.on_event("startup")
async def startup():
    await init_db()
    app.state.redis = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
    asyncio.create_task(run_bot())  # Запускаем бота в фоне


def run_fastapi():
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

async def bot_startup(bot):
    print('======================== БОТ ВКЛЮЧЕН =============================')

@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()

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











