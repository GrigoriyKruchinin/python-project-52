#!/usr/bin/env bash
# Выход при ошибке
set -o errexit

# Установка зависимостей с помощью poetry
poetry install

# Сбор статических файлов
python manage.py collectstatic --no-input

# Применение миграций
python manage.py migrate

# Компиляция сообщений для локалей
python manage.py compilemessages