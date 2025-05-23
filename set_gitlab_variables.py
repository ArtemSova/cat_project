import requests
from config import *

# Скрипт записывает или обновляет переменные в GitLab. (masked переменные скрипт не обновит)

# Токен В GitLab: User settings → Access tokens с правами api
# ID В URL проекта: https://gitlab.com/username/projectname → нажми Settings → General → Project ID
GITLAB_TOKEN = GITLAB_TOKEN  # Или впиши строку токена сюда
PROJECT_ID = PROJECT_ID  # ID проекта на GitLab
GITLAB_API = "https://gitlab.com/api/v4"
DB_HOST = DB_HOST
DB_PORT = DB_PORT
DB_USER = DB_USER
DB_PASS = DB_PASS
DB_NAME = DB_NAME
BOT_TOKEN = BOT_TOKEN
ADMINS_LIST = ADMINS_LIST
BOT_ADDRESS = BOT_ADDRESS
DOCKER_USERNAME = DOCKER_USERNAME
DOCKER_PASSWORD = DOCKER_PASSWORD
DEPLOY_USER = DEPLOY_USER
DEPLOY_SERVER_IP = DEPLOY_SERVER_IP

headers = {
    "PRIVATE-TOKEN": GITLAB_TOKEN,
    "Content-Type": "application/json"
}

# ✅ Список переменных
variables = {
    "DB_HOST": DB_HOST,
    "DB_PORT": DB_PORT,
    "DB_USER": DB_USER,
    "DB_PASS": DB_PASS,
    "DB_NAME": DB_NAME,
    "REDIS_HOST": "redis",
    "REDIS_URL": "redis://redis:6379/0",
    "BOT_TOKEN": BOT_TOKEN,
    "ADMINS_LIST": ADMINS_LIST,
    "BOT_ADDRESS": BOT_ADDRESS,
    "DOCKER_USERNAME": DOCKER_USERNAME,
    "DOCKER_PASSWORD": DOCKER_PASSWORD,
    "DEPLOY_USER": DEPLOY_USER,
    "DEPLOY_SERVER_IP": DEPLOY_SERVER_IP,
    "SSH_PRIVATE_KEY": """-----BEGIN OPENSSH PRIVATE KEY-----
b3__я_пока_не_знаю_как_передать_этот_ключ_через_окружение_dsvsdvdsgtZW
Qy__я_пока_не_знаю_как_передать_этот_ключ_через_окружение_AJBKm1wgSptc
IA__я_пока_не_знаю_как_передать_этот_ключ_через_окружение_hDFlqiIo+/BQ
AA__я_пока_не_знаю_как_передать_этот_ключ_через_окружение_2G5b3+E/Vekc
XOL6HXMFGEMWWqIij78FAAAACWdpdGxhYi1jaQECAwQ=-----END OPENSSH PRIVATE KEY-----""".replace("\n", "\\n")

}


def set_variable(key, value):
    url = f"{GITLAB_API}/projects/{PROJECT_ID}/variables/{key}"
    payload = {
        "value": value,
        "variable_type": "env_var",
        "protected": False,
        "masked": False  # Маскируй только пароли или ключи с max 100 символами
    }

    r = requests.put(url, headers=headers, json=payload)

    if r.status_code == 404:
        # Если переменной нет — создаём
        create_url = f"{GITLAB_API}/projects/{PROJECT_ID}/variables"
        create_payload = {**payload, "key": key}
        r = requests.post(create_url, headers=headers, json=create_payload)
        if r.status_code == 201:
            print(f"✅ {key} created")
        else:
            print(f"❌ Failed to create {key}: {r.status_code} - {r.text}")
    elif r.status_code == 200:
        print(f"🔁 {key} updated")
    else:
        print(f"❌ Failed to update {key}: {r.status_code} - {r.text}")

for key, value in variables.items():
    set_variable(key, value)


'''
Выполнение файла
python set_gitlab_variables.py
'''

