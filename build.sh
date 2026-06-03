#!/usr/bin/env bash
# Render build script — выполняется перед стартом веб-сервиса.
# Порядок: установка зависимостей → сборка статики → миграции → seed-данные.

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py migrate

# Создаём роли если ещё не существуют (идемпотентно)
python manage.py shell -c "
from core.models import Role
for name in ('admin', 'manager', 'client'):
    Role.objects.get_or_create(name=name)
print('Roles OK')
"
