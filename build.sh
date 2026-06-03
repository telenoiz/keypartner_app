#!/usr/bin/env bash
# Render build script — выполняется перед стартом веб-сервиса.
# Порядок: установка зависимостей → сборка статики → миграции → seed-данные.

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Заполняем справочники и демо-пользователей (идемпотентно)
python manage.py seed_data
