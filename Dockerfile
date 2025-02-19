# Базовый образ с Python 3.11
FROM python:3.11

# Устанавливаем зависимости для Poetry
RUN apt-get update && apt-get install -y curl

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

# Добавляем путь Poetry в ENV (чтобы Docker видел команду poetry)
ENV PATH="/root/.local/bin:$PATH"

# Указываем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости через Poetry
RUN poetry install --no-root

# Запуск сервера Django
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]