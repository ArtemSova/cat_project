# Приложение просмотра котиков (FastAPI + aiogram + PosgreSQL)

### Приложение находится в процессе разработки, доработки и расширения функций

## Функции FastAPI:
* Авторизация / Аутентификация через cookie
* Просмотр списка котиков на главной странице (без авторизации)
* Добавление новых котиков (только авторизованным пользователям)
* Добавлен Redis: кэширование запросов в БД

## Функции Телеграм-бота:
* Просмотр списка котиков
* Добавление новых котиков
* регистрация на сайте (в FastAPI), создание пароля для аутентификации