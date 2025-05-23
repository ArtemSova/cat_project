import json
import secrets
import uuid
from datetime import datetime
from http.client import HTTPException
from typing import Annotated, Any

from redis import asyncio as aioredis
from fastapi import APIRouter, Depends, Request, Form, HTTPException, status, Response, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse

from app.orm import *
from app.models import Cats


router = APIRouter(prefix="/cats", tags=["Cats Api"])
templates = Jinja2Templates(directory="templates")

security = HTTPBasic()

# временное хранилище кук о пользователях, которые авторизовались
COOKIES: dict[str, dict[str, Any]] = {}
# Ключ для куки из которого их читаем (может быть любая строчка)
COOKIE_SESSION_ID_KEY = "web-app-session-id"


# Функция для подключения к redis
async def get_redis(request: Request) -> aioredis.Redis:
    return request.app.state.redis


# функция проверки совпадения логина и пароля
async def get_auth_user_name(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: AsyncSession = Depends(get_db),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Неверный логин или пароль",
        headers={"WWW-Authenticate": "Basic"},
    )
    # получаем пароль из БД по введенному username
    stmt = select(Users.password).where(Users.user_name == credentials.username)
    result = await db.execute(stmt)
    psswrd = result.scalar_one_or_none()

    # проверяем есть ли username в БД (иначе пароль не придет)
    if psswrd is None:
        raise unauthed_exc    # возвращает общую ошибку(неверен логин или пароль)

    # сравниваем пароли из БД и от пользователя
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        psswrd.encode("utf-8"),
    ):
        raise unauthed_exc

    return credentials.username

# генератор уникального id сессии для кук
async def generate_session_id() -> str:
    return uuid.uuid4().hex

# функция для получения данных из куки о пользователе
async def get_session_data(
        session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован"
        )
    return COOKIES[session_id]

#-----------------------------------------ручки-------------------------------------------------

# ручка для основной страницы со всеми котиками
@router.get("/all_cats")
async def all_cats(
        request: Request,
        redis: aioredis.Redis = Depends(get_redis),
        db: AsyncSession = Depends(get_db)  # Нужно добавить отдельную зависимость для сессии
):
    # Попытка получить данные из Redis
    all_cats_data = await redis.get("all_cats")

    if not all_cats_data:
        cats = await orm_all_cats()
        if not cats:
            raise HTTPException(status_code=404, detail="No cats found")

        # Сериализовать данные для Redis
        cats_data = [{
            "cat_name": cat.cat_name,
            "cat_color": cat.cat_color,
            "cat_age": cat.cat_age,
            "cat_rating": cat.cat_rating
        } for cat in cats]

        all_cats_data = json.dumps(cats_data)
        await redis.set("all_cats", all_cats_data, ex=3600)  # Кэшировать на 1 час

    # Десериализовать данные из кэша
    cats = json.loads(all_cats_data)

    return templates.TemplateResponse("cats.html", {"request": request, "cats": cats})

# ручка для отображения конкретного котика
@router.get("/{cat_name}")
async def read_one_cat(
        cat_name: str,
        redis: aioredis.Redis = Depends(get_redis)
):
    # Попытка получить данные из Redis
    cat_data = await redis.get(cat_name)
    if not cat_data:
        # Если данных нет в Redis, получить их из основного источника
        cat = await orm_one_cat(cat_name)
        if not cat:
            raise HTTPException(status_code=404, detail="Cat not found")

        # Сохранить данные в Redis
        cat_data = json.dumps({
            "cat_name": cat.cat_name,
            "cat_color": cat.cat_color,
            "cat_age": cat.cat_age,
            "cat_rating": cat.cat_rating
        })
        await redis.set(cat_name, cat_data, ex=3600)  # Кэшировать на 1 час

    # выгружаем данные в ручку уже из сохраненного кэша, а не из запроса orm
    cat = json.loads(cat_data)
    return JSONResponse(content={
        "Имя Котика": cat["cat_name"],
        "Цвет Котика": cat["cat_color"],
        "Возраст Котика": cat["cat_age"],
        "Рейтинг Котика": cat["cat_rating"]
    })

''' Если надо выгружать данные из запроса
    return JSONResponse(content={
        "Имя Котика": cat.cat_name,
        "Цвет Котика": cat.cat_color,
        "Возраст Котика": cat.cat_age,
        "Рейтинг Котика": cat.cat_rating,
    })
'''


# ручка для базовой аторизации (принимает логин и пароль)
@router.get("/basic-auth/")
async def basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    return {
        "message": "Hi",
        "username": credentials.username,
        "password": credentials.password,
    }


# ручка авторизации с сохранением в куки (получает логин/пароль из ручки basic_auth_credentials, запускает проверку get_auth_user_name, и сохраняет данные в куку)
@router.get("/login_cookie/")
async def get_user_name_cookie(
    response: Response,
    auth_username: str = Depends(get_auth_user_name),
):
    session_id = str(await generate_session_id())
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": str(datetime.now()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "ok"}

# ручка для разлогинивания
@router.get("/logout-cookie/")
async def logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"Goodbye {username}!",
    }


# @router.get("/create")
# async def create_cat_form(request: Request):
#     return templates.TemplateResponse("create_cat.html", {"request": request})

@router.post("/create")
async def create_cat(
    user_session_data: dict = Depends(get_session_data),
    cat_name: str = Form(...),
    cat_color: str = Form(...),
    cat_age: int = Form(...),
    db: AsyncSession = Depends(get_db),
):
    if user_session_data:
        new_cat = Cats(cat_name=cat_name, cat_color=cat_color, cat_age=cat_age)
        db.add(new_cat)
        await db.commit()
        return RedirectResponse(url="/all_cats/", status_code=303)
    raise HTTPException(status_code=403, detail="Forbidden")




# функция с быстрой проверкой пользователя в аргументе (для тестирования)
@router.get("/check-cookie")
async def auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"Hello {username}!",
        **user_session_data
    }

