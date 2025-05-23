FROM python:3.13-slim

# Объявляем аргументы чтобы их видел контейнер
ARG DB_HOST
ARG DB_PORT
ARG DB_USER
ARG DB_PASS
ARG DB_NAME
ARG REDIS_HOST
ARG REDIS_URL
ARG BOT_TOKEN
ARG ADMINS_LIST
ARG BOT_ADDRESS

# Переводим их в переменные окружения
ENV DB_HOST=${DB_HOST} \
    DB_PORT=${DB_PORT} \
    DB_USER=${DB_USER} \
    DB_PASS=${DB_PASS} \
    DB_NAME=${DB_NAME} \
    REDIS_HOST=${REDIS_HOST} \
    REDIS_URL=${REDIS_URL} \
    BOT_TOKEN=${BOT_TOKEN} \
    ADMINS_LIST=${ADMINS_LIST} \
    BOT_ADDRESS=${BOT_ADDRESS}

# Теперь они доступны в RUN командах
RUN echo "DB_USER = $DB_USER" && \
    echo "REDIS_HOST = $REDIS_HOST"

# директория в контейнере, куда будет ставиться приложение
WORKDIR /app

# копировать все файлы
COPY . .

RUN pip install -r requirements.txt

# Порт, на котором будет работать апи
EXPOSE 8000

CMD ["python", "main.py"]
