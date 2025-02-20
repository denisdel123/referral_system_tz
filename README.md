# referral_system_tz

## Как работать с проектом:
Установка Poetry (если не установлен):
Для brew (macOS)
```
brew install poetry
```

Или официальный скрипт(macOS и Linux):
```
curl -sSL https://install.python-poetry.org | python3 -
```

Перезапускаем терминал и проверяем наличие poetry:
```
poetry --version
```

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:denisdel123/referral_system_tz.git
```
```
cd referral_system_tz
```

Создать и активировать виртуальное окружение:
```
poetry shell
```

Установить зависимости:
```
poetry install --no-root
```

В корне проекта создать файл .env
```
touch .env
```

```
и заполнить его по .env.exemple
```

```
Выполнить миграции
```
```
python manage.py makemigrations
python manage.py migrate
```

```
запустить с помощью docker:
docker compose up --build
```