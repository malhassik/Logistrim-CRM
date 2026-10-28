# Берем легковесный образ Python
FROM python:3.12-slim

# Переменные окружения (чтобы не создавались .pyc файлы и логи шли сразу в консоль)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая папка внутри контейнера
WORKDIR /app

# Копируем и устанавливаем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . /app/

# Открываем порт
EXPOSE 8000

# Команда по умолчанию (перезапишем в docker-compose)
CMD ["gunicorn", "logistrim.wsgi:application", "--bind", "0.0.0.0:8000"]