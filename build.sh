#!/usr/bin/env bash
# Устанавливаем зависимости
pip install -r requirements.txt

# Собираем статику
python manage.py collectstatic --no-input

# Применяем миграции к базе данных
python manage.py migrate