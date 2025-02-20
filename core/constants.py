import os

from dotenv import load_dotenv

load_dotenv()

# Ключ проекта
SECRET_KEY = os.environ.get("SECRET_KEY")

# переменные .env
POSTGRES_DB = os.environ.get("POSTGRES_DB", 'django')
POSTGRES_USER = os.environ.get("POSTGRES_USER", 'django')
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", '')
DB_HOST = os.environ.get("DB_HOST", '')
DB_PORT = os.environ.get("DB_PORT", 5432)

DEBUG = os.environ.get("DEBUG", "False") == "True"

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND")
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# константы проекта
NULLABLE = {
    'blank': True,
    'null': True
}

CHAR_LENGTH = 50

CHAR_LENGTH_REFERRAL = 10
