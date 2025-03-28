FROM python:3.13-slim

# копировать все файлы
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]