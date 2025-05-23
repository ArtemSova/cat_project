import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

REDIS_URL = os.getenv("REDIS_URL")

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMINS_LIST = os.getenv("ADMINS_LIST")
BOT_ADDRESS = os.getenv("BOT_ADDRESS")

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
PROJECT_ID = os.getenv("PROJECT_ID")
DOCKER_USERNAME = os.getenv("DOCKER_USERNAME")
DOCKER_PASSWORD = os.getenv("DOCKER_PASSWORD")
DEPLOY_USER = os.getenv("DEPLOY_USER")
DEPLOY_SERVER_IP = os.getenv("DEPLOY_SERVER_IP")



