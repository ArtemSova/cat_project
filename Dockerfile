FROM python:3.13-slim

# директория в контейнере, куда будет ставиться приложение
WORKDIR /app

# копировать все файлы
COPY . .

RUN pip install -r requirements.txt

# Порт, на котором будет работать апи
EXPOSE 8000

CMD ["python", "main.py"]